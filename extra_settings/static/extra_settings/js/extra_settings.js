/*global django*/

(function($) {
    // console.log("init");

    $(document).ready(function() {
        // console.log("ready");
        var resultsEl = $("#changelist-form .results");
        var tableEl = resultsEl.find("#result_list");
        var colsEl = tableEl.find("thead tr");
        var colEl;
        var rowsEl = tableEl.find("tbody tr");
        var rowEl;
        var valueType;

        // hide values cols headers
        colsEl.each(function(index, el) {
            colEl = $(el);
            colEl.find("*[class^='column-value_']").css("display", "none");
        });

        // add generic value col header
        var valueColText = colsEl.find("th").last().text();
        var valueColHTML = "<th><div class='text'><span>" + valueColText + "</span></div><div class='clear'></div></th>";
        var valueColEl = $(valueColHTML);
        colsEl.append(valueColEl);

        // hide unnecessary value cols from each row
        rowsEl.each(function(index, el) {
            rowEl = $(el);
            valueType = rowEl.find(".field-value_type").text();
            // console.log(index, el, valueType);
            if (valueType !== "") {
                rowEl.find("*[class^='field-value_']").not(String(".field-value_" + valueType)).css("display", "none");
            }
        });

        // show back the changelist
        resultsEl.addClass("extra-settings-ready");
    });

})(django.jQuery || window.jQuery);
