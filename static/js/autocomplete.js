function autocomplete(search_url) {
    const AUTOCOMPLETE_ITEMS_LIMIT = 10;

    $(document).ready(function () {
        let search_input = $("#search_input");

        search_input.keyup(function () {
            let search = $(this).val();
            updateAutocompleteList(search);
        });


        search_input.focus(function () {
            showList();
        });

        search_input.blur(function () {
            setTimeout(hideList, 100);

        });

    })

    function showList() {
        $('#autocomplete-items').show();
    }

    function hideList() {
        $('#autocomplete-items').hide();
    }

    function updateAutocompleteList(search) {
        let autocompleteItems = $('#autocomplete-items');
        if (search.length > 2) {
            $.ajax({
                url: search_url,
                type: 'GET',
                data: {search: search},
                dataType: 'json',
                success: function (response) {
                    let result = response['result']
                    autocompleteItems.empty();
                    let length = Math.min(AUTOCOMPLETE_ITEMS_LIMIT, result.length);
                    for (let i = 0; i < length; i++) {
                        let name = result[i]['name'];
                        let url = result[i]['url'];
                        let is_vegan = result[i]['is_vegan'];

                        autocompleteItems.append(createListItem(name, url, is_vegan));
                    }
                }
            })
        } else {
            autocompleteItems.empty();
        }
    }

    function createListItem(name, url, is_vegan) {
        let item = `<a href="${url}"><div>${name}`;
        if (is_vegan) {
            item += '<span style="color:green">(V)</span>';
        } else {
            item += '<span style="color:red">(not V)</span>';
        }
        item += '</div></a>'

        return item;
    }
}