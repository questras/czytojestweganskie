function autocomplete(search_url) {
    const AUTOCOMPLETE_ITEMS_LIMIT = 10;

    $(document).ready(function () {
        let search_input = $("#search_input");

        // Update autocomplete list when search input is changed.
        search_input.keyup(function () {
            let search_query = $(this).val();
            updateAutocompleteList(search_query);
        });

        // Show autocomplete list when search input gets focused.
        search_input.focus(function () {
            showAutocompleteList();
        });

        // Hide autocomplete list 100ms after search input gets unfocused.
        search_input.blur(function () {
            setTimeout(hideAutocompleteList, 100);
        });
    })

    function showAutocompleteList() {
        $('#autocomplete-items').show();
    }

    function hideAutocompleteList() {
        $('#autocomplete-items').hide();
    }

    function updateAutocompleteList(search_query) {
        let autocompleteList = $('#autocomplete-items');

        // Show autocomplete list only when there are more than 2 characters
        // in search input.
        if (search_query.length > 2) {
            $.ajax({
                url: search_url,
                type: 'GET',
                data: {search_query: search_query},
                dataType: 'json',
                success: function (response) {
                    let result = response['result'];
                    autocompleteList.empty();
                    let length = Math.min(AUTOCOMPLETE_ITEMS_LIMIT, result.length);
                    for (let i = 0; i < length; i++) {
                        let name = result[i]['name'];
                        let url = result[i]['url'];
                        let image_url = result[i]['image_url'];
                        let is_vegan = result[i]['is_vegan'];

                        autocompleteList.append(
                            createListItem(name, url, image_url, is_vegan)
                        );
                    }
                }
            })
        }
        else {
            autocompleteList.empty();
        }
    }

    function createListItem(name, url, image_url, is_vegan) {
        let is_vegan_span;
        if (is_vegan) {
            is_vegan_span = '<span style="color:green">(V)</span>';
        }
        else {
            is_vegan_span = '<span style="color:red">(not V)</span>';
        }

        return `<a href="${url}">
                <div class="autocomplete-item">
                    <img src="${image_url}">
                    <div>${name}${is_vegan_span}</div>
                </div>
                </a>`;
    }
}