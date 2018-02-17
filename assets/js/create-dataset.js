/*****************************************
* Custom Javascript to Create Dataset
*/

var datasetAjaxUrl = {
	post: "/api/v1/datasets/"
};

(function($) {

	/////////////////////////////////////
	// custom functions

	$.extend({

		// check token
		csrf_safe_method: function(method) {
			// these HTTP methods do not require CSRF protection
			return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
		},

		// AJAX modules ---------
		post_dataset: function(data, callback, errorCallback) {
			// ajax
			$.ajax({
				type       : "POST",
				url        : datasetAjaxUrl.post,
				data       : data,
				dataType   : "json",
				beforeSend : function(jqXHR) {
					$("body").addClass("loading");

					var csrftoken = $("[name=csrfmiddlewaretoken]").val();

					if (!$.csrf_safe_method("POST") && !this.crossDomain) {
						jqXHR.setRequestHeader("X-CSRFToken", csrftoken);
					}
				},
				complete   : function(jqXHR, textStatus) {
					// make delay for animation effect
					setTimeout(function() {
						$("body").removeClass("loading");
					}, 300);
				},
				error      : function(jqXHR, textStatus, errorThrown) {
					if(errorCallback) {
						errorCallback(jqXHR, textStatus, errorThrown);
					}
				},
				success    : function(response, textStatus, jqXHR) {
					if(callback) {
						callback(response);
					}
				}
			});
		}
	});

	////////////////////////////////////////////

	// save table
	$(document).on("click", "#new-dataset-col", function(e) {
		e.preventDefault();

		var tpl = $($(this).data("tpl")).html(),
			formWrap = $($(this).data("target"));

		$(tpl).appendTo(formWrap).hide().slideDown(300);
	});

	// save table
	$(document).on("click", "#create-dataset", function(e) {
		e.preventDefault();

		var form = $("#new-dataset-form"),
			title = $("#dataset-title"),
			desc = $("#dataset-desc"),
			cols = $("#new-col-form");

		// validation
		var invalid = 0;
		form.find("[required]").each(function() {
			if(!$(this).val()) {
				invalid++;
			}
		});

		if(invalid > 0) {
			alert("Please fill up required fields, for example, title, column name");
			return false;
		}

		// bind data to submit
		var data = {
			name:        title.val(),
			description: desc.val(),
			column_names: {}
		};

		cols.find(".new-col").each(function() {
			var colName = $(this).children("[name=\"col-name\"]").val(),
				colDesc = $(this).children("[name=\"col-desc\"]").val();

			if(colName) {
				data.column_names[colName] = colDesc;
			}
		});

		data.column_names = JSON.stringify(data.column_names);
		// console.log(JSON.stringify(data));

		// submit data
		$.post_dataset(
			data, 
			function(response) { // success callback
				// alert("New Dataset is submitted successfully");
				location.href = '/dataset/detail_dataset/' + response.pk + '/';
			},
			function() { // error callback
				alert("New Dataset is not submitted correctly.");
			}
		);
	});

	/////////////////////////////////////////
	// init form when document-ready
	$(document).ready(function() {
		if ($("#new-dataset-col").length) {
			$("#new-dataset-col").trigger("click");
		}
	});
})(jQuery);