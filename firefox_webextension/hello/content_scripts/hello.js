(function() {

  /**
   * On vérifie et on initialise une variable globale
   * permettant de s'assurer que le script ne fera rien
   * s'il est injecté plusieurs fois sur la page.
   */
  if (window.hasRun) {
    return;
  }
  window.hasRun = true;

  console.log('*** Init ***');
  
  document.addEventListener("click", (e) => {
    console.log('*** hello ***');

    // https://developer.mozilla.org/fr/docs/Mozilla/Add-ons/WebExtensions/API/tabs/query
    function logTabs(tabs) {
      for (let tab of tabs) {
        // tab.url requires the `tabs` permission
        console.log(tab.url);
      }
    }
    
    function onError(error) {
      console.log(`Error: ${error}`);
    }
    
    var querying = browser.tabs.query({});
    querying.then(logTabs, onError);
  });

})();
