//Return the docker container IP for the given container name
def getIPFor( containername ) {
serviceip = sh (
script: "sudo docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ${containername}",
returnStdout: true
).trim()
if (serviceip != '') {
return serviceip
} else {
error("Coult not obtain service ip for container " + containername + ". Got this value: '" + serviceip + "'")
}
}

//Build the url for the given service
def buildServicePath( containername, port, path ) {
ip = getIPFor(containername)
return 'http://' + ip + ':' + port + path
}

node(params.deploynode) {
properties([
parameters([
string(
defaultValue: "add_submit_button", 
description: 'Which branch of app to use', 
name: 'deployBranch'
),
string(
defaultValue: "gdchdpmn02drlx.geisinger.edu", 
description: 'The node on which container runs', 
name: 'deploynode'
)
])
])
// Define IP address as null to avoid cache issues where an IP is set, but not actually available
CHIMEAPP_URL = ''
// NODECONTENT_URL = ''
// PUBLISHPDF_URL = ''
// NOTESHANDLER_URL = ''
// PATIENTDETAILS_URL = ''
// PATIENTDETAILSPDF_URL = ''
currentBuild.result = "SUCCESS"
try {
stage('Checkout') {			
dir('chime') {
git url: 'https://github.com/GeisingerHealthSystem/chime', credentialsId: 'udahadoopops', branch: params.deployBranch
}
}
stage('Initializing vars') {			
sh script: """
echo "CHIMEAPP_URL: '${CHIMEAPP_URL}'"			
"""
}
// stage('Build decom-ui') {
// // sh 'mkdir -p ghs-sys-decom/docker/nodejs-node-decomui/target'
// // sh 'cp ghs-sys-decom/decom-ui/package.json ghs-sys-decom/docker/nodejs-node-decomui/target/'
// // sh 'cp -a ghs-sys-decom/decom-ui/public ghs-sys-decom/docker/nodejs-node-decomui/target/'
// // sh 'cp -a ghs-sys-decom/decom-ui/src ghs-sys-decom/docker/nodejs-node-decomui/target/'
// // sh 'cp -a ghs-sys-decom/decom-ui/server ghs-sys-decom/docker/nodejs-node-decomui/target/'
//}
stage('Build docker') {

// sh 'cp -a ghs-sys-decom/config/dev ghs-sys-decom/docker/nodejs-node-decomui/cfg'
// dir('ghs-sys-decom/docker/nodejs-node-decomui') {
CHIMEAPP_URL = buildServicePath('chimeservice', '8080', '/chime')
// NODECONTENT_URL = buildServicePath('nodecontentservice', '8080', '/nodecontent')
// PUBLISHPDF_URL = buildServicePath('publishpdfservice', '8080', '/publishpdf')
// NOTESHANDLER_URL = buildServicePath('noteshandlerservice', '8080', '/noteshandler')
// PATIENTDETAILS_URL = buildServicePath('patientdetailsservice', '8080', '/patientdetails/')
// PATIENTDETAILSPDF_URL = buildServicePath('patientdetailspdfservice', '8080', '/patientdetails/')
sh script: """
sudo docker build -f Dockerfile -t docker/chime-app \
--build-arg CHIMEAPP_URL=${CHIMEAPP_URL} \
.
"""
}

stage('Start docker service') {

// withCredentials([usernamePassword(
// credentialsId: 'uda_adldap_svc',
// passwordVariable: 'AD_PASSWORD',
// usernameVariable: 'AD_USERNAME')]) {
sh 'echo Starting docker service'
sh script: '''
name='chime'
if [[ $(sudo docker ps -f "name=$name" --format '{{.Names}}') == $name ]]
then
sudo docker stop $name
sudo docker rm $name
else
if [[ $(sudo docker ps -f "status=exited" -f "name=$name" --format '{{.Names}}') == $name ]]
then
sudo docker rm $name
fi
fi
sudo docker run -td --name $name --hostname $name.geisinger.edu \
--network sysdecom-network \
-p 127.0.0.1:50202:3001 docker/chime-app
'''


sh 'echo Docker service started'

}
stage('Cleanup') {
cleanWs()
}
}
catch (err) {
currentBuild.result = "FAILURE"
throw err
}
finally {
String buildColor = 'YELLOW'
if (currentBuild.result == "SUCCESS") {
buildColor = 'GREEN'
}
if (currentBuild.result == "FAILURE") {
buildColor = 'RED'
}
cleanWs()
}
}