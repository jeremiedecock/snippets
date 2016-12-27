/*
 * See: https://developer.mozilla.org/fr/docs/Web/JavaScript/Guide/Nombres_et_dates#L%27objet_Date
 *      https://developer.mozilla.org/fr/docs/Web/JavaScript/Reference/Objets_globaux/Date
 */

var time = new Date();
var hours   = time.getHours();
var minutes = time.getMinutes();
var seconds = time.getSeconds();

print(time)
print(hours, minutes, seconds)
