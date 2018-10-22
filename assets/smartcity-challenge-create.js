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

var soundArr = [
{val : 'NO_SOUND', text: 'NO_SOUND'},
{val : 'STEAM_TRAIN_HORN', text: 'STEAM_TRAIN_HORN'},
{val : 'COURT_HOUSE', text: 'COURT_HOUSE'},
{val : 'CASH_REGISTER', text: 'CASH_REGISTER'},
{val : 'DOG_BARK', text: 'DOG_BARK'},
{val : 'PHONE_RINGING', text: 'PHONE_RINGING'},
{val : 'CHALKBOARD', text: 'CHALKBOARD'},
{val : 'SCHOOL_BELL', text: 'SCHOOL_BELL'},
{val : 'APPLAUSE', text: 'APPLAUSE'},
{val : 'BABY_CRYING', text: 'BABY_CRYING'},
{val : 'BEACH', text: 'BEACH'},
{val : 'BEACH_BALL', text: 'BEACH_BALL'},
{val : 'BIKE_BELL', text: 'BIKE_BELL'},
{val : 'BINGO', text: 'BINGO'},
{val : 'BOAT_HORN', text: 'BOAT_HORN'},
{val : 'BREWING_COFFEE', text: 'BREWING_COFFEE'},
{val : 'BUS', text: 'BUS'},
{val : 'CAR_DRIVING', text: 'CAR_DRIVING'},
{val : 'CAR_SOUND', text: 'CAR_SOUND'},
{val : 'CAT_MEOWING', text: 'CAT_MEOWING'},
{val : 'CHEERING', text: 'CHEERING'},
{val : 'DENTIST_DRILL', text: 'DENTIST_DRILL'},
{val : 'DINOSAUR', text: 'DINOSAUR'},
{val : 'DOLPHIN', text: 'DOLPHIN'},
{val : 'DOORBELL', text: 'DOORBELL'},
{val : 'ELECTRICITY', text: 'ELECTRICITY'},
{val : 'ELEVATOR_DING', text: 'ELEVATOR_DING'},
{val : 'ENVELOPE_RUSTLING', text: 'ENVELOPE_RUSTLING'},
{val : 'FIRE_TRUCK', text: 'FIRE_TRUCK'},
{val : 'FOOD_SIZZLING', text: 'FOOD_SIZZLING'},
{val : 'KEYBOARD_TYPING', text: 'KEYBOARD_TYPING'},
{val : 'LASER_TAG', text: 'LASER_TAG'},
{val : 'LAWNMOWER', text: 'LAWNMOWER'},
{val : 'MOO', text: 'MOO'},
{val : 'OMNINOUS_MUSIC', text: 'OMNINOUS_MUSIC'},
{val : 'OVERTIMER', text: 'OVERTIMER'},
{val : 'POWER_DRILL', text: 'POWER_DRILL'},
{val : 'ROOSTER', text: 'ROOSTER'},
{val : 'RUSTLING_LEAVES', text: 'RUSTLING_LEAVES'},
{val : 'SEAGULLS', text: 'SEAGULLS'},
{val : 'SEWAGE', text: 'SEWAGE'},
{val : 'SHHHH', text: 'SHHHH'},
{val : 'SIREN', text: 'SIREN'},
{val : 'SLOT_MACHINE', text: 'SLOT_MACHINE'},
{val : 'SLURPPING_STRAW', text: 'SLURPPING_STRAW'},
{val : 'SODA_CAN', text: 'SODA_CAN'},
{val : 'SPRINKLER', text: 'SPRINKLER'},
{val : 'WATER', text: 'WATER'},
]


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
{val : 'OLED_1', text: 'OLED_1'},
{val : 'OLED_2', text: 'OLED_2'},
{val : 'OLED_3', text: 'OLED_3'},
{val : 'OLED_4', text: 'OLED_4'},
{val : 'OLED_5', text: 'OLED_5'},
{val : 'OLED_6', text: 'OLED_6'},
{val : 'OLED_7', text: 'OLED_7'},
{val : 'OLED_8', text: 'OLED_8'},
{val : 'OLED_9', text: 'OLED_9'},
{val : 'S1_T1', text: 'S1_T1'},
{val : 'S1_T2', text: 'S1_T2'},
{val : 'S2_T1', text: 'S2_T1'},
{val : 'S4_T1', text: 'S4_T1'},
{val : 'MARINA', text: 'MARINA'},
{val : 'STREET_LIGHT', text: 'STREET_LIGHT'},
{val : 'TRAIN_STATION', text: 'TRAIN_STATION'},
{val : 'WEST_EAST', text: 'WEST_EAST'},
{val : 'NORTH_SOUTH', text: 'NORTH_SOUTH'},
{val : 'WINDMILL', text: 'WINDMILL'},
{val : 'UTILITY_POLE', text: 'UTILITY_POLE'}
];

var i = 0;
var sel = $('<select type=""number" class="form-control chal-buildingId" name="buildingId[' + i  + ']">').prependTo('.smart');
$(arr).each(function() {
 sel.append($("<option>").attr('value',this.val).text(this.text));
 sel.append($(' <span class="input-group-btn"><button type="button" class="btn btn-default btn-add">+</button></span>'));
});



var sel = $('<select type=""number" class="form-control chal-soundId" name="soundId">').appendTo('.sound');
$(soundArr).each(function() {
 sel.append($("<option>").attr('value',this.val).text(this.text));
});

(function ($) {
    $(function () {

        var addFormGroup = function (event) {
            event.preventDefault();
            i++;
            var $formGroup = $(this).closest('.form-group');
            var $multipleFormGroup = $formGroup.closest('.multiple-form-group');
            var $formGroupClone = $formGroup.clone();
	    var formExtract = $formGroupClone.find('select')
	    var newBuildingId = "buildingId[" + i + "]"
	    formExtract.attr("name", newBuildingId)
	    console.log(formExtract)
	    //var selectInput = $formGroupClon.getElementsByClassName('chal-buildingId')[0];
 	    
            $(this)
                .toggleClass('btn-default btn-add btn-danger btn-remove')
                .html('–');

            $formGroupClone.find('input').val('');
            $formGroupClone.insertAfter($formGroup);

            var $lastFormGroupLast = $multipleFormGroup.find('.form-group:last');
            if ($multipleFormGroup.data('max') <= countFormGroup($multipleFormGroup)) {
                $lastFormGroupLast.find('.btn-add').attr('disabled', true);
            }
        };

        var removeFormGroup = function (event) {
            event.preventDefault();

            var $formGroup = $(this).closest('.form-group');
            var $multipleFormGroup = $formGroup.closest('.multiple-form-group');

            var $lastFormGroupLast = $multipleFormGroup.find('.form-group:last');
            if ($multipleFormGroup.data('max') >= countFormGroup($multipleFormGroup)) {
                $lastFormGroupLast.find('.btn-add').attr('disabled', false);
            }

            $formGroup.remove();
        };

        var countFormGroup = function ($form) {
            return $form.find('.form-group').length;
        };

        $(document).on('click', '.btn-add', addFormGroup);
        $(document).on('click', '.btn-remove', removeFormGroup);

    });
})(jQuery);
