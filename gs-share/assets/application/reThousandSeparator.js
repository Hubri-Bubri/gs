export default function (value) {
    var transformValue = value.split('.').join('')
    transformValue = parseFloat(transformValue.split(',').join('.'))
    return transformValue;
}