/*
 * See: http://www.w3schools.com/js/js_json.asp
 */

var text = '{ "employees" : [' +
    '{ "firstName":"John" ,  "lastName":"Doe" },' +
    '{ "firstName":"Anna" ,  "lastName":"Smith" },' +
    '{ "firstName":"Peter" , "lastName":"Jones" } ]}';

var obj = JSON.parse(text);

print(obj.employees[0].firstName)
