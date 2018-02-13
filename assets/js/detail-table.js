/*****************************************
* Custom Javascript
*/
var ajaxUrlRoot = "",
	ajaxUrl = {};


(function($) {

	/////////////////////////////////////
	// custom functions

	$.extend({
		table_row_tpl: "",

		change_url: function(url) {
            url = url.replace(/^\/|\/$/g, "");

            var rootUrl = window.location.protocol + "//" + window.location.hostname + ":" + window.location.port + "/";
			ajaxUrlRoot = rootUrl + url + "/";
			ajaxUrl = {
				get      : ajaxUrlRoot,
				getAll   : ajaxUrlRoot + "{id}/",
				put      : ajaxUrlRoot + "{id}/",
				post     : ajaxUrlRoot,
				getOrder : rootUrl + "api/v1/orders/{id}/"
			};

			var t = url.match(/^api\/v1\/order\/(\d+)\/data/);

			if(!t.length || typeof(t[1]) == "undefined") {
				return ;
			}

			$.get_order_data(parseInt(t[1]), function(data) {
				var nameElem = $("#dataset-name"),
					descElem = $("#dataset-desc");

				if(data.name) {
					nameElem.text(data.name);
				} else {
					nameElem.text(nameElem.data("placeholder"));
				}

				if(data.description) {
					descElem.text(data.description);
				} else {
					descElem.text(descElem.data("placeholder"));
				}
			});
		},

		// check token
		csrf_safe_method: function(method) {
			// these HTTP methods do not require CSRF protection
			return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
		},

		// make template for each rows
		init_row_tpl: function(cols) {
			var row = "";

			for(var i in cols) {
				var attrs = "data-field=\"" + cols[i] + "\"",
					html = "";

				switch(cols[i]) {
					case "number":
						attrs += " data-id=\"##id##\"";
						html = "##index##";
						break;
					case "vegetarian":
						attrs += " data-elem=\"checkbox\" data-org=\"##" + cols[i] + "##\"";
						html = "\
							<input type=\"checkbox\" id=\"vegetarian_##index##\" value=\"##is_vegetarian##\" ##is_vegetarian_checked##>\
							<label for=\"vegetarian_##index##\" data-val=\"true\">Yes</label>\
							<label for=\"vegetarian_##index##\" data-val=\"false\">No</label>\
						";
						break;
					default:
						attrs += " data-org=\"##" + cols[i] + "##\" contenteditable=\"true\"";
						html = "##" + cols[i] + "##";
						break;
				}

				row += "<td " + attrs + ">" + html + "</td>";
			}

			$.table_row_tpl = row;
			return row;
		},

		// AJAX modules ---------
		get_order_data: function(orderId, callback, errorCallback) {
			// ajax
			$.ajax({
				type         : "GET",
				url          : ajaxUrl.getOrder.replace("{id}", orderId),
				dataType     : "json",
				jsonCallback : "callback",
				beforeSend   : function(jqXHR) {
					$("body").addClass("loading");
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
		},

		get_table_data: function(callback, errorCallback) {
			// ajax
			$.ajax({
				type         : "GET",
				url          : ajaxUrl.get,
				dataType     : "json",
				jsonCallback : "callback",
				beforeSend   : function(jqXHR) {
					$("body").addClass("loading");
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
		},

		put_table_data: function(data, callback, errorCallback) {
			// ajax
			$.ajax({
				type         : "PUT",
				url          : ajaxUrl.put.replace("{id}", data.id),
				data         : data,
				dataType     : "json",

				beforeSend   : function(jqXHR) {
					// using jQuery
					  var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

					  if (!$.csrf_safe_method("PUT") && !this.crossDomain) {
						  jqXHR.setRequestHeader("X-CSRFToken", csrftoken);
					  }

					$("body").addClass("loading");
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
		},

		post_table_data: function(data, callback, errorCallback) {
			// ajax
			$.ajax({
				type         : "POST",
				url          : ajaxUrl.post,
				data         : data,
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

		// initializing table data, add rows from data that is got from server
		init_table : function() {
			var table = $(this),
				tbody = table.children("tbody").html(""); // remove all original rows

			// define row template
			$.init_row_tpl(table.get_cols());

			// callback after ajax calling
			$.get_table_data(function(data) {
				for(var i in data) {
					data[i] = Object.assign({
						index                 : parseInt(i) + 1,
						vegetarian            : data[i].is_vegetarian,
						is_vegetarian_checked : data[i].is_vegetarian? "checked": ""
					}, data[i]);

					$("<tr></tr>").appendTo(tbody).print_row(data[i]);
				}
			},
			function() {
				alert("Invalid URL!");
			});

			return table;
		},

		// get columns info
		get_cols: function() {
			// get columns info
			var cols = [];

			$(this).children("thead").last("tr").find("[data-col]").each(function() {
				cols.push($(this).data("col"));
			});

			return cols;
		},

		// get row html from row template and row data
		print_row: function(data) {
			var row_html = $.table_row_tpl;

			for(var i in data) {
				var regex = new RegExp("##" + i + "##", "g");
				row_html = row_html.replace(regex, data[i]);
			}

			return $(this).html(row_html);
		},

		// get row data
		get_row: function(table) {
			var cols = table.get_cols(),
				data = {};

			for(var i in cols) {
				var td = $(this).find("td[data-field=\"" + cols[i] + "\"]");

				if(!td.length) {
					continue;
				}

				switch(cols[i]) {
					case "number":
						data.id = td.data("id");
						break;
					case "vegetarian":
						data.is_vegetarian = td.children("input[type=\"checkbox\"]").prop("checked");
						break;
					default:
						data[cols[i]] = td.text();
						break;
				}
			}

			return data;
		} 
	});

	////////////////////////////////////////////
	// Event callbacks

	$(document).on("click", "[data-order-id]", function(e) {
		var ulrElem = $("#api-key-url"),
			url = "/api/v1/order/" + $(this).data("order-id") + "/data/";
		if(ulrElem.length) {
			ulrElem.val(url);

			$('.dataset_name').text($(this).text());

			$.change_url(url);
			$("#image-data-table").init_table();
		}
	});

	// change url and initialize table while change api key url
	$(document).on("change", "#api-key-url", function(e) {
		var url = $(this).val();

		if(/api\/v1\/order\/[0-9]+\/data/.test(url)) {
			$.change_url(url);
			$("#image-data-table").init_table();
		} else {
			alert("Please enter API Key URL correctly.");
		}
	});

	// save table
	$(document).on("click", ".new-row", function() {
		var table = $("#image-data-table"),
			tbody = table.children("tbody"),
			cols = table.get_cols(),
			data = {};

		for(var i in cols) {
			data[cols[i]] = "";
		}

		data = Object.assign({
			id                    : 0,
			index                 : tbody.find("tr").length + 1,
			vegetarian            : false,
			is_vegetarian_checked : ""
		}, data);

		// add new row
		$("<tr></tr>").appendTo(tbody).attr("data-row", "new").print_row(data);
	});

	// save table
	$(document).on("click", ".save-table", function() {
		var table = $("#image-data-table"),
			tbody = table.children("tbody"),
			cols = table.get_cols(),
			data = {};

		tbody.find("tr").each(function() {
			
			// new row
			if($(this).data("row") == "new") {

				data = $(this).get_row(table);
				$.post_table_data(
					data, 
					function(response) { // success callback
						console.log("New row data is submitted successfully", response);
					},
					function() { // error callback
						alert("New row is not submitted correctly.");
					});
				
				$(this).data("row", "");

			} else {

				// detect changed row
				var changed = false;
				$(this).find("[data-org]").each(function() {
					var org = $(this).data("org");

					switch($(this).data("field")) {
						case "vegetarian":
							var state = $(this).children("input[type=\"checkbox\"]").prop("checked");
							if(org != state) {
								changed = true;

								// reset original data by new data
								$(this).data("org", state);
							}
							break;
						default:
							var state = $(this).text();
							if(org != $(this).text()) {
								changed = true;

								// reset original data by new data
								$(this).data("org", state);
							}
							break;
					}
				});

				if(changed) {
					data = $(this).get_row(table);
					
					$.put_table_data(
						data, 
						function(response) { // success callback
							console.log("Changed row data is submitted successfully", response);
						},
						function() { // error callback
							alert("Changed row is not submitted correctly.");
						});
				}
			}
		});
	});

	/////////////////////////////////////////
	// init form when document-ready
	$(document).ready(function() {

		//$("#image-data-table").init_table();

	});
})(jQuery);