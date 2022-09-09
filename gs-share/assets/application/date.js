export default function (value) {
    var output = ''
    if((value==null)||(value==undefined)||(value=='')){
        output = 'not set'
    }
    else{
        if ((value.split('-').length)+(value.split(' ').length==4)) {
            var separate = value.split('-')
            output = separate[2]+'.'+separate[1]+'.'+separate[0];
        }

        if ((value.split('-').length)+(value.split(' ').length)==5) {
            var sp = value.split(' ')[0]
            var separate = sp.split('-')
            output = separate[2]+'.'+separate[1]+'.'+separate[0]+' '+value.split(' ')[1];
        }
    }
    return output
}