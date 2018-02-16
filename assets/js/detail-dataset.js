/*****************************************
* Custom Javascript
*/

// var sampleCols = {
// 		"title": "dataset title",
// 		"description": "its description",
// 		"column_names": {
// 			"Column 1": "descirption",
// 			"Column 2": "descirption",
// 			"Column 3": "descirption",
// 			"Column 4": "descirption",
// 			"Column 5": "descirption"
// 		}
// 	},
// 	sampleData = [
// 		{
// 			"Column 1": "Aget 1",
// 			"Column 2": "Customer",
// 			"Column 3": "weight",
// 			"Column 4": "Vgetarian",
// 			"Column 5": "56"
// 		},
// 		{
// 			"Column 1": "Aget 2",
// 			"Column 2": "Customer2",
// 			"Column 3": "weight2",
// 			"Column 4": "Vgetaria2n",
// 			"Column 5": "526"
// 		},
// 		{
// 			"Column 1": "Aget 3",
// 			"Column 2": "Cust3ome4",
// 			"Column 3": "weight4",
// 			"Column 4": "Vgetarian4",
// 			"Column 5": "564"
// 		},
// 	];

(function($) {

	var api_url = $('#api-url--text').val(),
		ajaxUrl = {
			get :   api_url,
			post:   api_url
		};

	/////////////////////////////////////
	// custom functions

	$.extend({
		table_row_tpl: "",

		// AJAX modules ---------

		// check token
		csrf_safe_method: function(method) {
			// these HTTP methods do not require CSRF protection
			return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
		},

		// get data by ajax
		get_dataset_data: function(callback, errorCallback) {
			// return callback(sampleData);

			// ajax
			$.ajax({
				type        : "GET",
				url         : ajaxUrl.get,
				dataType    : "json",
				beforeSend  : function(jqXHR) {
					$("body").addClass("loading");
				},
				complete    : function(jqXHR, textStatus) {
					// make delay for animation effect
					setTimeout(function() {
						$("body").removeClass("loading");
					}, 300);
				},
				error       : function(jqXHR, textStatus, errorThrown) {
					if(errorCallback) {
						errorCallback(jqXHR, textStatus, errorThrown);
					}
					// body...
				},
				success     : function(response, textStatus, jqXHR) {
					if(callback) {
						callback(response);
					}
				}
			});
		},

		// post data
		post_dataset_data: function(data, callback, errorCallback) {
			// ajax
			$.ajax({
				type         : "POST",
				url          : ajaxUrl.post,
				data         : {
					data: JSON.stringify(data)
				},
				dataType     : "json",
				beforeSend   : function(jqXHR) {
					$("body").addClass("loading");

					var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

					if (!$.csrf_safe_method("POST") && !this.crossDomain) {
						jqXHR.setRequestHeader("X-CSRFToken", csrftoken);
					}
				},
				complete     : function(jqXHR, textStatus) {
					// make delay for animation effect
					setTimeout(function() {
						$("body").removeClass("loading");
					}, 300);
				},
				error        : function(jqXHR, textStatus, errorThrown) {

					if(errorCallback) {
						errorCallback(jqXHR, textStatus, errorThrown);
					}
					// body...
				},
				success      : function(response, textStatus, jqXHR) {
					if(callback) {
						callback(response);
					}
				}
			});
		}
	});

	// functions for "this" object
	$.fn.extend({

		// make template for each rows
		init_dataset_table: function(data) {
			var table = $(this),
				tbody = table.children("tbody");

			// add table data
			for(var r in data) {
				var tr = $("<tr>").appendTo(tbody);

				// add number column
				$("<td>").appendTo(tr).text(parseInt(r) + 1).attr("data-number");

				for(var c in data[r]) {
					$("<td>").appendTo(tr).text(data[r][c]).attr({"contenteditable": true, "data-field": c});
				}
			}

			return table;
		},

		// initializing table data, add rows from data that is got from server
		init_table : function() {
			var table = $(this); // remove all original rows

            // add tbody
			if(!table.children("tbody").length) {
				$("<tbody>").appendTo(table);
			}

            // callback after ajax calling
			$.get_dataset_data(function(response) {
				if(response.data.length) {
					table.init_dataset_table(response.data);
				}
			}, function(jqXHR, textStatus, errorThrown) {
				console.log("ERROR", jqXHR);
			});

			
			return table;
		},

		// create new row
		new_row: function() {
			var table = $(this),
				thead = table.children("thead"),
				tbody = table.children("tbody"),
				newRow = thead.html().replace(/th/g, "td");

			$(newRow).appendTo(tbody).find("td").each(function() {
				if($(this).data("field")) {
					$(this).text("").attr("contenteditable", true);
				} else {
					$(this).text(tbody.children("tr").length);
				}
			});

			return table;
		},

		// save dataset table
		save_dataset: function() {
			var table = $(this),
				tbody = table.children("tbody"),
				data = [];

			tbody.find("tr").each(function() {
				var fields = $(this).find("td[data-field]"),
					emptyValNum = 0,
					row = {};

				fields.each(function() {
					var field = $(this).data("field");

					row[field] = $(this).text();

					if(!row[field]) {
						emptyValNum++;
					}
				});

				if(fields.length > emptyValNum) {
					data.push(row);
				}
			});

			console.log(data);

			if(data.length) {
				$.post_dataset_data(data, function() {
					alert("Dataset is saved successfully");
				}, function(jqXHR, textStatus, errorThrown) {
					console.log("ERROR", jqXHR);
				});
			} else {
				alert("Please enter table data.");
			}

			return table;
		}
	});


	/////////////////////////////////////////
	// init form when document-ready

	$(document).on("click", "#copy-clipboard", function(e) {
		e.preventDefault();

		/* Get the text field */
		var copyText = $(this).prev("input")[0];

		/* Select the text field */
		copyText.select();

		/* Copy the text inside the text field */
		document.execCommand("Copy");

		/* Alert the copied text */
		alert("Copied the text: " + copyText.value);
	});


	$(document).ready(function() {
		if($("#dataset-table").length) {
			$("#dataset-table").init_table();

			// add new row
			$("#dataset-newrow").on("click", function() {
				$("#dataset-table").new_row();
			});

			// save table
			$("#dataset-save").on("click", function() {
				$("#dataset-table").save_dataset();
			});
		}
	});
})(jQuery);