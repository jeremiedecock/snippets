function getCurrentWindowTabs() {
  //return browser.tabs.query({currentWindow: true});
  //return browser.tabs.query({});
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

/**
 * Fired when a registered command is activated using a keyboard shortcut.
 *
 * In this sample extension, there is only one registered command: "Ctrl+Shift+U".
 * On Mac, this command will automatically be converted to "Command+Shift+U".
 */
browser.commands.onCommand.addListener((command) => {
  listTabs();
});
