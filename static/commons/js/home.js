export function setCookie() {
    let reportRef = document.getElementById("reportRef").value
    document.cookie = "report_ref=" + reportRef;
    let reportPath = window.location.protocol + "//" + window.location.host + "/"
    window.location = reportPath
}

export function goHome() {
    let homePath = window.location.protocol + "//" + window.location.host + "/home"
    window.location = homePath
    document.cookie = "report_ref=;"
    window.history.pushState('data', 'title', '/');
}