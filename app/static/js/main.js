const language = "en"

$('input.dateinput').datepicker({
    format: "dd/mm/yyyy",
    language: language,
    minViewMode: 0,
    autoclose: true,
    todayHighlight: true
});

$('input.dateinput_d').datepicker({
    format: "dd",
    language: language,
    autoclose: true,
    todayHighlight: true
});

$('input.dateinput_m').datepicker({
    format: "mm",
    minViewMode: 1,
    language: language,
    autoclose: true
});

$('input.dateinput_y').datepicker({
    format: "yyyy",
    minViewMode: 2,
    language: language,
    autoclose: true
});