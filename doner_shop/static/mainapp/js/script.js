var orderType = document.getElementById('id_order_type')
var paymentType = document.getElementById('id_payment_type')
var deliveryName = document.getElementById('id_delivery_name')

deliveryName.disabled = true

function orderTypeChoice() {
    var orderTypeIndex = orderType.options[orderType.selectedIndex].text
//    console.log(orderTypeIndex)
    
    if (orderTypeIndex == 'На месте') {
        paymentType.disabled = false
        deliveryName.disabled = true
    }
    if (orderTypeIndex == 'Доставка') {
        paymentType.disabled = true
        deliveryName.disabled = false
    }
    if (orderTypeIndex == 'Персонал'){
        paymentType.disabled = true
        deliveryName.disabled = true
    }
}

orderType.addEventListener('change', orderTypeChoice)