function preprocessVehicleTitle(vehicle_title) {
    let lowercasedString = vehicle_title.toLowerCase();
    let words = lowercasedString.split(' ');

    if (words.includes("bmw")) {
        return [words[1], "seria-" + words[2]];
    }

    if (words.includes("rover") && words.includes("land")) {
        if (words.includes("range")) {
            return [words[1] + "-" + words[2], words[3] + "-" + words[4]];
        }
        return [words[1] + "-" + words[2], words[3]];
    }
    return [words[1], words[2]]

    // Mercedes
}


function openAutovitPage(title, mileage, price, horsepower) {
    var brand_and_model = preprocessVehicleTitle(title)
    var autovitURL = `https://www.autovit.ro/autoturisme/${brand_and_model[0]}/${brand_and_model[1]}?search%5Bfilter_float_engine_power%3Afrom%5D=${horsepower}&search%5Bfilter_float_mileage%3Ato%5D=${mileage}&search%5Bfilter_float_price%3Ato%5D=${price}&search%5Badvanced_search_expanded%5D=true`;
    window.open(autovitURL);
}
