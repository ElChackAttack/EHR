var settings = {
    rows: 10,
    cols: 15,
    rowCssPrefix: 'row-',
    colCssPrefix: 'col-',
    seatWidth: 72,
    seatHeight: 80,
    seatCss: 'seat',
    selectedSeatCss: 'selectedSeat',
    selectingSeatCss: 'selectingSeat',
};
var init = function (reservedSeat) {
     var str = [], seatNo, className;
     for (i = 0; i < settings.rows; i++) {
         for (j = 0; j < settings.cols; j++) {
             seatNo = (i + j * settings.rows + 1);
             className = settings.seatCss + ' ' + settings.rowCssPrefix + i.toString() + ' ' + settings.colCssPrefix + j.toString();
             if ($.isArray(reservedSeat) && $.inArray(seatNo, reservedSeat) != -1) {
                 className += ' ' + settings.selectedSeatCss;
             }
             str.push('<li class="' + className + '"' +
                       'style="top:' + (i * settings.seatHeight).toString() + 'px;left:' + (j * settings.seatWidth).toString() + 'px">' +
                       '<a title="' + seatNo + '">' + seatNo + '</a>' +
                       '</li>');
         }
     }
     $('#place').html(str.join(''));
 };
//case I: Show from starting
//init();

//Case II: If already booked
var bookedRooms = {{full_rooms | safe}};
var allRooms = {{full_rooms | safe}};
var maxSelected = 0;
init(bookedRooms);
$('.' + settings.seatCss).click(function () {
if ($(this).hasClass(settings.selectedSeatCss)){
alert('This room is already reserved');
}   
else{
if(maxSelected == 0){
 $(this).toggleClass(settings.selectingSeatCss);
 maxSelected = 1;
}
else if (maxSelected == 1 && $(this).hasClass(settings.selectingSeatCss)){
 $(this).toggleClass(settings.selectingSeatCss);
 maxSelected = 0;
}

else{
 maxSelected = 1;
}
}
});

$('#btnShowNew').click(function () {
var str = [], item;
$.each($('#place li.' + settings.selectingSeatCss + ' a'), function (index, value) {
item = $(this).attr('title');                   
str.push(item);                   
});
alert(str.join(','));
})