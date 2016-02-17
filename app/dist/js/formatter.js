/**
 * Format Icons
 *
 */

function invTypeIconFormatter(value) {
    return '<img src="http://imageserver.eveonline.com/Type/' + value + '_32.png">';
}

function characterIconFormatter(value) {
    return '<img src="http://imageserver.eveonline.com/Character/' + value + '_256.jpg" width=32px height=32px>';
}

function allianceIconFormatter(value) {
    return '<img src="http://imageserver.eveonline.com/Alliance/' + value + '_32.png">';
}

function corporationIconFormatter(value) {
    return '<img src="http://imageserver.eveonline.com/Corporation/' + value + '_32.png">';
}

function numberCom(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function numberDec(x) {
    return x.toFixed(2).replace(/(\d)(?=(\d{3})+\.)/g, '$1,');
}