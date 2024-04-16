function updateQuantity(productId, action) {
    fetch('/update_quantity/' + productId + '/' + action + '/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        },
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        if (data.status === 'success') {
            // Actualizează vizual cantitatea produsului pe pagină (dacă este necesar)
            // Poți utiliza DOM manipulation pentru acest lucru

            // De exemplu, dacă ai un element HTML cu id-ul 'quantity_' + productId
            // poți actualiza textul acestuia cu noua cantitate primită de la server:
            // document.getElementById('quantity_' + productId).innerText = data.new_quantity;

            window.location.reload(); // Reîncarcă pagina pentru a actualiza informațiile
        } else {
            console.error('Eroare la actualizarea cantității produsului:', data.message);
        }
    })
    .catch(error => {
        console.error('Eroare la comunicarea cu serverul:', error);
    });
}


function deleteProduct(productId) {
    fetch('/delete_product/' + productId, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        },
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);

        if (data.status === 'success') {

            const row = document.getElementById(`order_item_${productId}`);
            if (row) {
                row.remove();
            }
            window.location.reload();
        } else {
            console.error('Eroare la ștergerea produsului:', data.message);
        }
    })
    .catch(error => {
        console.error('Eroare la comunicarea cu serverul:', error);
    });
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).on("click", ".add_to_wishlist", function(){
    let productId = $(this).attr("data-product-item");
    let this_val = $(this);

    console.log("Product ID is", productId);

    $.ajax({
        url: "add_to_wishlist/",
        data: {
            "id": productId
        },
        dataType: "json",
        beforeSend: function() {
            this_val.html('<i class="fas fa-check"></i>'); // Afișează o bifa din Font Awesome
        },
        success: function(response, status) {
            if (response.bool === true) {
                // Aici poți adăuga cod pentru a manipula DOM-ul dacă adăugarea la lista de dorințe a avut succes
            }
        },
        error: function(xhr, errmsg, err) {
            console.error("Eroare la comunicarea cu serverul:", errmsg);
        }
    });
});
//
//function getCategories() {
//    fetch('/get_categories/', {
//        method: 'GET',
//        headers: {
//            'X-CSRFToken': getCookie('csrftoken'),
//        },
//    })
//    .then(response => response.json())
//    .then(data => {
//        console.log(data);
//        // Aici poți actualiza DOM-ul pentru a afișa categoriile obținute
//    })
//    .catch(error => {
//        console.error('Eroare la obținerea categoriilor:', error);
//    });
//}

