// Markdown Preview
$('#desc-edit').on('shown.bs.tab', function (event) {
    if (event.target.hash === '#desc-preview'){
        $(event.target.hash).html(marked($('#desc-editor').val(), {'gfm':true, 'breaks':true}));
    }
});
$('#new-desc-edit').on('shown.bs.tab', function (event) {
    if (event.target.hash === '#new-desc-preview'){
        $(event.target.hash).html(marked($('#new-desc-editor').val(), {'gfm':true, 'breaks':true}));
    }
});
$("#solve-attempts-checkbox").change(function() {
    if(this.checked) {
        $('#solve-attempts-input').show();
    } else {
        $('#solve-attempts-input').hide();
        $('#max_attempts').val('');
    }
});

$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
});


var arr = [
{val : 'S1_B01', text: 'S1_B01'},
{val : 'S1_B02', text: 'S1_B02'},
{val : 'S1_B03', text: 'S1_B03'},
{val : 'S1_B04', text: 'S1_B04'},
{val : 'S1_B05', text: 'S1_B05'},
{val : 'S2_B01', text: 'S2_B01'},
{val : 'S2_B02', text: 'S2_B02'},
{val : 'S2_B03', text: 'S2_B03'},
{val : 'S2_B04', text: 'S2_B04'},
{val : 'S2_B05', text: 'S2_B05'},
{val : 'S2_B06', text: 'S2_B06'},
{val : 'S2_B07', text: 'S2_B07'},
{val : 'S2_B08', text: 'S2_B08'},
{val : 'S2_B09', text: 'S2_B09'},
{val : 'S2_B10', text: 'S2_B10'},
{val : 'S2_B11', text: 'S2_B11'},
{val : 'S2_B12', text: 'S2_B12'},
{val : 'S2_B13', text: 'S2_B13'},
{val : 'S2_B14', text: 'S2_B14'},
{val : 'S2_B15', text: 'S2_B15'},
{val : 'S2_B16', text: 'S2_B16'},
{val : 'S2_B17', text: 'S2_B17'},
{val : 'S2_B18', text: 'S2_B18'},
{val : 'S2_B19', text: 'S2_B19'},
{val : 'S2_B20', text: 'S2_B20'},
{val : 'S2_B21', text: 'S2_B21'},
{val : 'S2_B22', text: 'S2_B22'},
{val : 'S2_B23', text: 'S2_B23'},
{val : 'S2_B24', text: 'S2_B24'},
{val : 'S2_B25', text: 'S2_B25'},
{val : 'S2_B26', text: 'S2_B26'},
{val : 'S3_B01', text: 'S3_B01'},
{val : 'S3_B02', text: 'S3_B02'},
{val : 'S3_B03', text: 'S3_B03'},
{val : 'S3_B04', text: 'S3_B04'},
{val : 'S3_B05', text: 'S3_B05'},
{val : 'S3_B06', text: 'S3_B06'},
{val : 'S3_B07', text: 'S3_B07'},
{val : 'S3_B08', text: 'S3_B08'},
{val : 'S3_B09', text: 'S3_B09'},
{val : 'S3_B10', text: 'S3_B10'},
{val : 'S3_B11', text: 'S3_B11'},
{val : 'S3_B12', text: 'S3_B12'},
{val : 'S3_B13', text: 'S3_B13'},
{val : 'S3_B14', text: 'S3_B14'},
{val : 'S4_B01', text: 'S4_B01'},
{val : 'S4_B02', text: 'S4_B02'},
{val : 'S4_B03', text: 'S4_B03'},
{val : 'S4_B04', text: 'S4_B04'},
{val : 'S4_B05', text: 'S4_B05'},
{val : 'S4_B06', text: 'S4_B06'},
{val : 'S4_B07', text: 'S4_B07'},
{val : 'S4_B08', text: 'S4_B08'},
{val : 'S4_B09', text: 'S4_B09'},
{val : 'S4_B10', text: 'S4_B10'},
{val : 'S4_B11', text: 'S4_B11'},
{val : 'S4_B12', text: 'S4_B12'},
{val : 'S4_B13', text: 'S4_B13'},
{val : 'S4_B14', text: 'S4_B14'},
{val : 'S4_B15', text: 'S4_B15'},
{val : 'S4_B16', text: 'S4_B16'},
{val : 'S4_B17', text: 'S4_B17'},
{val : 'S5_B01', text: 'S5_B01'},
{val : 'S5_B02', text: 'S5_B02'},
{val : 'S5_B03', text: 'S5_B03'},
{val : 'S5_B04', text: 'S5_B04'},
];

var sel = $('<select type=""number" class="form-control chal-buildingId" name="buildingId">').appendTo('.smart');
$(arr).each(function() {
 sel.append($("<option>").attr('value',this.val).text(this.text));
});


