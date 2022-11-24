


map.eachLayer(layer => layer.addEventListener("click", (e) => {
    // On récupère la valeur de la ville recherchée
    // const term = e.currentTarger.lat
    // console.log(term)
    console.log(layer)
    const term = layer._popup._content
    console.log(layer._popup._content)

    // On récupère les informations de la ville recherchée sur l'url qu'on a en back
    fetch(`/?site=${term}`).then(
        response => response.json()
    ).then(responseData => {
        displayInfoo(responseData)
        console.log('Success', responseData)
    }).catch((err) => {
        console.error("Error !!!", err)
    })
})
)



function displayInfoo(site) {
    //on suppirme les card avant de les ajouter
    const cardPrevious = document.getElementById("card")
    if (cardPrevious) {
        cardPrevious.remove()
    }
    const card = document.createElement("div")
    card.classList.add("card", "col", "raw-mb-8", "mt-4")
    card.setAttribute("id", "card")

    card.innerHTML = `
        <div>
            <img class="card-img-top " src="${site.photo}" height="300px" style="object-fit: contain;"alt="Card image cap">
            <div class="card-body">
                <h5 class="card-title"> ${site.nom}(<small>${site.pays}, ${site.continent}</small>) <i class="tim-icons icon-pin"></i></h5>
                <p class="card-text">${site.description}</p>
                <a href="${site.wiki}" target='_blank' class="btn btn-info">
                    <i class="tim-icons icon-zoom-split"></i>
                    Plus d'informations</a>
                <a href="https://www.coordonnees-gps.fr/street-view/@${site.coord},h0,p0,z0" target='_blank' class="btn btn-primary">
                    <i class="tim-icons icon-square-pin"></i>
                    Visiter sur streetView
                </a>
            </div>
        </div>
    `

    document.getElementById("displayInfoSite").appendChild(card)


    return card
}
