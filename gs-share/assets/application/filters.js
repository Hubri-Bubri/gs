export default function (value) {
    var value = Math.round(value * 100) / 100
    var parts = (value + '').split('.');
    var main = parts[0];
    var len = main.length;
    var output = '';
    var i = len - 1;
    while (i >= 0) {
        output = main.charAt(i) + output;
        if ((len - i) % 3 === 0 && i > 0) {
            output = '.' + output;
        }
        --i;
    }

    if (parts.length > 1) {
        output += ',' + parts[1];
        if (parts[1].length==1) output += '0'
    }else{
        output += ',00'
    }
    return output;
}