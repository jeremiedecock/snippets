function getCurrentWindowTabs() {
  //return browser.tabs.query({currentWindow: true});
  // return browser.tabs.query({});
  return browser.tabs.query({currentWindow: true, highlighted: true});  // Copy only selected tabs
}

function listTabs() {
  getCurrentWindowTabs().then((tabs) => {
    let tabsListStr = "";
    for (let tab of tabs) {
      tabsListStr += `- [${ tab.title }](${ tab.url })\n`;
    }

    navigator.clipboard.writeText(tabsListStr).then(function() {
      alert("Presse-papiers modifié avec succès\n");
    }, function() {
      alert("Échec de l’écriture dans le presse-papiers\n");
    });
  });
}

document.addEventListener("click", (e) => {

  if (e.target.id === "tabs-list") {
    listTabs();
  }

  e.preventDefault();
});
