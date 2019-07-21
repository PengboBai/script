#!/groovy
static main(String[] args) {
    timestamps {
        pipeline_build()
    }
}

def pipeline_build(){
    revision = env.REVISION
    diff = env.diff
    repo_uri = env.repo_uri
    stage_uri = env.stage_uri
    jenkins_url = env.BUILD_URL

    stage("echo info"){
        println "REVISION: ${revision}\n" + 
        "DIFF: ${diff}\n" +
        "REPO_URI: ${repo_uri}\n" +
        "STAGE_URI: ${stage_uri}\n" +
        "JENKINS_URL: ${jenkins_url}" 
    }

    stage("update code"){
        build job: 'BeforeUpdateCode', parameters: [string(name: 'REVISION', value: "${revision}"),
            string(name: 'DIFF', value: "${diff}"), string(name: 'REPO_URI', value: "${repo_uri}"),
            string(name: 'STAGE_URI', value: "${stage_uri}")]
    }

    stage("build") {
        build job: 'BeforeBuild', parameters: [string(name: 'REVISION', value: "${revision}"),
            string(name: 'DIFF', value: "${diff}"), string(name: 'REPO_URI', value: "${repo_uri}"),
            string(name: 'STAGE_URI', value: "${stage_uri}"), string(name: 'JENKINS_URL', value: "${jenkins_url}")]
    }
}