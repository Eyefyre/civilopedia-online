var current_language = "en"
var translations = {}
var data_mappings = {}
var current_category = "cat_1"
var current_section = "sec_1"
var current_item = "item_37"
var content_mapping = []

var tag_mappings = {
    "[NEWLINE]": "<br>",
    "[TAB]": "&nbsp;",
    "[ICON_HAPPINESS_1]": "<img class='icon align-top' src='/assets/images/icon_images/ICON_HAPPINESS_1.png'>",
    "[ICON_HAPPINESS_4]": "<img class='icon align-top' src='/assets/images/icon_images/ICON_HAPPINESS_4.png'>",
    "[ICON_CULTURE]": "<img class='icon align-top' src='/assets/images/icon_images/ICON_CULTURE.png'>",
    "[ICON_INTERNATIONAL_TRADE]": "<img class='icon align-top' src='/assets/images/icon_images/ICON_INTERNATIONAL_TRADE.png'>",
    "[ICON_GOLD]": "<img class='icon align-top' src='/assets/images/icon_images/ICON_GOLD.png'>",
    "[COLOR_POSITIVE_TEXT]": "<span style='color:#7FFF19'>",
    "[ENDCOLOR]": "</span>",
    "[ICON_TOURISM]": "<img class='icon align-top' src='/assets/images/icon_images/ICON_TOURISM.png'>",
    "[ICON_PEACE]": "<img class='icon align-top' src='/assets/images/icon_images/ICON_PEACE.png'>",
    "[ICON_FOOD]": "<img class='icon align-top' src='/assets/images/icon_images/ICON_FOOD.png'>",
    "[ICON_PRODUCTION]": "<img class='icon align-top' src='/assets/images/icon_images/ICON_PRODUCTION.png'>",
    "[ICON_RESEARCH]": "<img class='icon align-top' src='/assets/images/icon_images/ICON_RESEARCH.png'>",
    "[ICON_RANGE_STRENGTH]": "<img class='icon align-top' src='/assets/images/icon_images/ICON_RANGE_STRENGTH.png'>",
    "[ICON_CONNECTED]": "<img class='icon align-top' src='/assets/images/icon_images/ICON_CONNECTED.png'>",
    "[ICON_INFLUENCE]": "<img class='icon align-top' src='/assets/images/icon_images/ICON_INFLUENCE.png'>",
    "[ICON_RES_WINE]": "<img class='icon align-top' src='/assets/images/icon_images/ICON_RES_WINE.png'>",
    "[ICON_RES_INCENSE]": "<img class='icon align-top' src='/assets/images/icon_images/ICON_RES_INCENSE.png'>",
    "[ICON_STRENGTH]": "<img class='icon align-top' src='/assets/images/icon_images/ICON_STRENGTH.png'>",
    "[ICON_GREAT_PEOPLE]": "<img class='icon align-top' src='/assets/images/icon_images/ICON_GREAT_PEOPLE.png'>",
    "[ICON_SPY]": "<img class='icon align-top' src='/assets/images/icon_images/ICON_SPY.png'>",
    "[ICON_RELIGION]": "<img class='icon align-top' src='/assets/images/icon_images/ICON_RELIGION.png'>",
    "[ICON_TROPHY_GOLD]": "<img class='icon align-top' src='/assets/images/icon_images/ICON_TROPHY_GOLD.png'>",
    "[ICON_TROPHY_SILVER]": "<img class='icon align-top' src='/assets/images/icon_images/ICON_TROPHY_SILVER.png'>",
    "[ICON_TROPHY_BRONZE]": "<img class='icon align-top' src='/assets/images/icon_images/ICON_TROPHY_BRONZE.png'>",
    "[ICON_CAPITAL]": "<img class='icon align-top' src='/assets/images/icon_images/ICON_CAPITAL.png'>",
    "[ICON_GOLDEN_AGE]": "<img class='icon align-top' src='/assets/images/icon_images/ICON_GOLDEN_AGE.png'>",
    "[ICON_CITIZEN]": "<img class='icon align-top' src='/assets/images/icon_images/ICON_CITIZEN.png'>",
    "[ICON_MOVES]": "<img class='icon align-top' src='/assets/images/icon_images/ICON_MOVES.png'>",
    "[ICON_DIPLOMAT]": "<img class='icon align-top' src='/assets/images/icon_images/ICON_DIPLOMAT.png'>",
    "[ICON_RES_URANIUM]": "<img class='icon align-top' src='/assets/images/icon_images/ICON_RES_URANIUM.png'>",
    "[ICON_RES_ALUMINUM]": "<img class='icon align-top' src='/assets/images/icon_images/ICON_RES_ALUMINUM.png'>",
    "[ICON_RES_COW]": "<img class='icon align-top' src='/assets/images/icon_images/ICON_RES_COW.png'>",
    "[ICON_RES_SHEEP]": "<img class='icon align-top' src='/assets/images/icon_images/ICON_RES_SHEEP.png'>",
    "[ICON_RES_HORSE]": "<img class='icon align-top' src='/assets/images/icon_images/ICON_RES_HORSE.png'>",
    "[ICON_RES_IRON]": "<img class='icon align-top' src='/assets/images/icon_images/ICON_RES_IRON.png'>",
    "[ICON_RES_MARBLE]": "<img class='icon align-top' src='/assets/images/icon_images/ICON_RES_MARBLE.png'>",
    "[ICON_RES_FISH]": "<img class='icon align-top' src='/assets/images/icon_images/ICON_RES_FISH.png'>",
    "[ICON_RES_PEARLS]": "<img class='icon align-top' src='/assets/images/icon_images/ICON_RES_PEARLS.png'>",
    "[ICON_RES_DEER]": "<img class='icon align-top' src='/assets/images/icon_images/ICON_RES_DEER.png'>",
    "[ICON_RES_IVORY]": "<img class='icon align-top' src='/assets/images/icon_images/ICON_RES_IVORY.png'>",
    "[ICON_RES_FUR]": "<img class='icon align-top' src='/assets/images/icon_images/ICON_RES_FUR.png'>",
    "[ICON_RES_TRUFFLES]": "<img class='icon align-top' src='/assets/images/icon_images/ICON_RES_TRUFFLES.png'>",
    "[ICON_OCCUPIED]": "<img class='icon align-top' src='/assets/images/icon_images/ICON_OCCUPIED.png'>",
}


document.addEventListener("DOMContentLoaded", async function () {
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
    $("body").hide()
    current_language = (sessionStorage.getItem("locale") || "en");
    await fetch("./assets/data/translations_" + current_language + ".json")
        .then(response => response.json())
        .then(data => {
            translations[current_language] = data;
        })
        .catch(error => console.error(`Error loading ${language} translation file:`, error));
    await fetch("./assets/data/structure.json")
        .then(response => response.json())
        .then(data => {
            data_mappings = data;
        })
        .catch(error => console.error(`Error loading ${language} structure file:`, error));
    await fetch("./assets/data/content.json")
        .then(response => response.json())
        .then(data => {
            content_mapping = data;
        })
        .catch(error => console.error(`Error loading ${language} content file:`, error));
    await $("#language-dropdown").val(current_language)
    await populate_dropdowns()
    current_category = data_mappings["categories"][0]
    current_section = current_category["sections"][0]
    current_item = current_section["items"][0]
    generate_view()
    create_listeners()
    set_heading()
    generate_accordion_list()
    $("body").show()
});


$(document).on('change', '#category-dropdown', function (e) {
    current_category = data_mappings["categories"].find(item => item.id === this.value);
    $("#section-dropdown").empty()
    for (var i = 0; i < current_category["sections"].length; i++) {
        if (i == 0) {
            $("#section-dropdown").append("<option selected value='" + current_category["sections"][i]["id"] + "'>" + get_translation(current_language, current_category["sections"][i]["label"]) + "</option>");
        }
        else {
            $("#section-dropdown").append("<option value='" + current_category["sections"][i]["id"] + "'>" + get_translation(current_language, current_category["sections"][i]["label"]) + "</option>");
        }
    }
    $('#section-dropdown').trigger('change');
});

$(document).on('change', '#section-dropdown', function (e) {
    current_section = current_category["sections"].find(item => item.id === this.value);
    $("#item-dropdown").empty()
    for (var i = 0; i < current_section["items"].length; i++) {
        if (i == 0) {
            $("#item-dropdown").append("<option selected value='" + current_section["items"][i]["id"] + "'>" + get_translation(current_language, current_section["items"][i]["label"]) + "</option>");
        }
        else {
            $("#item-dropdown").append("<option value='" + current_section["items"][i]["id"] + "'>" + get_translation(current_language, current_section["items"][i]["label"]) + "</option>");
        }
    }
    $('#item-dropdown').trigger('change');
});

$(document).on('change', '#item-dropdown', function (e) {
    current_item = current_section["items"].find(item => item.id === this.value);
    generate__mobile_view()
});


async function populate_dropdowns() {
    $("#category-dropdown").empty()
    for (var i = 0; i < data_mappings["categories"].length; i++) {
        if (i == 15) {
            $("#category-dropdown").append("<option selected value='" + data_mappings["categories"][i]["id"] + "'>" + get_translation(current_language, data_mappings["categories"][i]["label"]) + "</option>");
        }
        else {
            $("#category-dropdown").append("<option value='" + data_mappings["categories"][i]["id"] + "'>" + get_translation(current_language, data_mappings["categories"][i]["label"]) + "</option>");
        }
    }
    current_category = data_mappings["categories"].find(item => item.id === $("#category-dropdown").val());
    $("#section-dropdown").empty()
    for (var i = 0; i < current_category["sections"].length; i++) {
        if (i == 1) {
            $("#section-dropdown").append("<option selected value='" + current_category["sections"][i]["id"] + "'>" + get_translation(current_language, current_category["sections"][i]["label"]) + "</option>");
        }
        else {
            $("#section-dropdown").append("<option value='" + current_category["sections"][i]["id"] + "'>" + get_translation(current_language, current_category["sections"][i]["label"]) + "</option>");
        }
    }
    current_section = current_category["sections"].find(item => item.id === $("#section-dropdown").val());
    $("#item-dropdown").empty()
    for (var i = 0; i < current_section["items"].length; i++) {
        if (i == 16) {
            $("#item-dropdown").append("<option selected value='" + current_section["items"][i]["id"] + "'>" + get_translation(current_language, current_section["items"][i]["label"]) + "</option>");
        }
        else {
            $("#item-dropdown").append("<option value='" + current_section["items"][i]["id"] + "'>" + get_translation(current_language, current_section["items"][i]["label"]) + "</option>");
        }
    }
    current_item = current_section["items"].find(item => item.id === $("#item-dropdown").val());
}

function get_translation(language, key) {
    //console.log("Getting Translation for " + key + " in " + language)
    if (key in translations[language]) {
        return parse_tags(translations[language][key])
    }
    else {
        //console.log(`\"${key}\" doesn't exist in ${language} file, parsing tags as plain`)
        return parse_tags(key)
    }

}

function parse_tags(text) {
    for (var key in tag_mappings) {
        text = text.replaceAll(key, tag_mappings[key])
    }
    var matches = text.match(/{([^}]*)}/g);
    for (match in matches) {
        text = text.replace(matches[match], get_translation(current_language, matches[match].replace("{", "").replace("}", "")))
    }
    return text
}

function create_listeners() {
    const buttons = document.querySelectorAll('.language-button');
    buttons.forEach(function (button) {
        button.addEventListener('click', function () {
            current_language = this.value
            sessionStorage.setItem("locale", current_language);
            $("body").hide()
            location.reload();
        });
    });
}

Handlebars.registerHelper('translate', function (aString) {
    //console.log("Handlebar Helper translate: " + aString)
    return get_translation(current_language, aString)
})

Handlebars.registerHelper('get_item_name', function (item_id) {
    item_name = get_info_from_item_id(item_id)["strings"]["title"]
    //console.log("Handlebar Helper Item Name: " + item_name)
    return item_name
})
Handlebars.registerHelper('get_item_image', function (item_id) {
    return get_info_from_item_id(item_id)["strings"]["image"]
})

Handlebars.registerHelper('parse_tags', function (aString) {
    return parse_tags(aString)
})

Handlebars.registerHelper('log_info', function (aString) {
    console.log(aString)
})

function generate_view() {
    $("#content-area").empty()
    var item_data = content_mapping.find(item => item.item_id === current_item.id);
    //console.log("Curent item is " + JSON.stringify(item_data))
    var template = Handlebars.compile($("#" + item_data["view_id"]).html())
    $("#content-area").append(template(item_data))
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
}

//Trigger on Category tab click
$(document).on("click", ".category-tab", function () {
    current_category = data_mappings["categories"].find(item => item.id === this.value);
    current_section = current_category["sections"][0]
    current_item = current_section["items"][0]
    set_heading()
    generate_accordion_list()
    
});

$(document).on("click", ".list-group-item", function () {
    current_section = current_category["sections"].find(item => item.id === $(this).parent().attr("value"));
    current_item = current_section["items"].find(item => item.id === $(this).attr("value"));
    console.log("current item = " + current_item["id"])
    if (["item_1", "item_2", "item_3", "item_4", "item_5", "item_6", "item_7", "item_8", "item_9", "item_10", "item_11", "item_12", "item_13", "item_14", "item_15", "item_16"].includes(current_item["id"])) {
        console.log("Checking home pages")
        check_home_pages()
    }    
    generate_view()
})

function switch_category() {
    console.log(current_category["id"])
    switch (current_category["id"]) {
        case "cat_1":
            document.querySelector('#home-tab').click();
            break;
        case "cat_2":
            document.querySelector('#concepts-tab').click();
            break;
        case "cat_3":
            document.querySelector('#tech-tab').click();
            break;
        case "cat_4":
            document.querySelector('#units-tab').click();
            break;
        case "cat_5":
            document.querySelector('#promos-tab').click();
            break;
        case "cat_6":
            document.querySelector('#buildings-tab').click();
            break;
        case "cat_7":
            document.querySelector('#wonders-tab').click();
            break;
        case "cat_8":
            document.querySelector('#social-tab').click();
            break;
        case "cat_9":
            document.querySelector('#great-tab').click();
            break;
        case "cat_10":
            document.querySelector('#civs-tab').click();
            break;
        case "cat_11":
            document.querySelector('#cities-tab').click();
            break;
        case "cat_12":
            document.querySelector('#terrain-tab').click();
            break;
        case "cat_13":
            document.querySelector('#resources-tab').click();
            break;
        case "cat_14":
            document.querySelector('#improvements-tab').click();
            break;
        case "cat_15":
            document.querySelector('#religion-tab').click();
            break;
        case "cat_16":
            document.querySelector('#congress-tab').click();
            break;
    }
}

function check_home_pages() {
    category_index = parseInt(current_item["id"].split("_")[1]) - 1
    current_category = data_mappings["categories"][category_index]
    current_section = current_category["sections"][0]
    current_item = current_section["items"][0]
    switch_category()
}


$(document).on("click", ".small-image", function () {
    //console.log($(this).attr("value"))
})

function set_heading() {
    $("#current_heading").text(get_translation(current_language, current_category["label"]));
    $("#civilopedia-title").text(get_translation(current_language, "TXT_KEY_CIVILOPEDIA"));
    $("#language-dropdown-desktop").text(get_translation(current_language, "TXT_KEY_OPSCREEN_SELECT_LANG"));
}

function generate_accordion_list() {
    $("#accordionExample").empty()
    var accordion_section = ""
    current_category["sections"].forEach((section, index) => {
        if (index == 0) {
            accordion_section = `<div class="accordion-item"><div id="collapseNone" class="accordion-collapse collapse show"><ul value=${section.id} class="list-group list-group-flush">`
            section["items"].forEach((item) => {
                accordion_section += `<li value=${item.id} class="list-group-item">${get_translation(current_language, item.label)}</li>`
            });
            accordion_section += `</ul></div></div>`
        }
        else {
            accordion_section = `<div class="accordion-item"><div class="accordion-header" id="heading${section.id}"><button class="accordion-button p-1 shadow-none" type="button" data-bs-toggle="collapse"
                data-bs-target="#collapse${section.id}" aria-expanded="true" aria-controls="collapse${section.id}">
                ${get_translation(current_language, section.label)}</button></div>
            <div id="collapse${section.id}" class="accordion-collapse collapse show" aria-labelledby="heading${section.id}">
              <ul value=${section.id} class="list-group list-group-flush">`
            section["items"].forEach((item) => {
                accordion_section += `<li value=${item.id} class="list-group-item">${get_translation(current_language, item.label)}</li>`
            });

            accordion_section += `</ul></div></div>`
        }
        $("#accordionExample").append(accordion_section)
    });
}


function get_info_from_item_id(item_id) {
    item_info = content_mapping.find(element => element.item_id === item_id);
    //console.log("Current item is " + item_info)
    return item_info
}