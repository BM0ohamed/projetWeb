// Je récupère la bar de recherche
const searchBar = document.getElementById("searchSite")
//on crée un groupe de marker vide pour les ajouter plus tard
const markerGroup = L.layerGroup().addTo(map)

// A chaque fois qu'il y a une nouvelle valeurs
searchBar.addEventListener("change", (e) => {
    // On récupère la valeur de la ville recherchée
    const term = e.currentTarget.value


    // On récupère les informations de la ville recherchée sur l'url qu'on a en back
    fetch(`/europe?site=${term}`).then(
        response => response.json()
    ).then(responseData => {
        // On crée une carte qui affiche les données ;)
        console.log(responseData.comments)
        displayInfoSite(responseData)
        // on vide le group de marker
        markerGroup.clearLayers()

        //on ajoute un marker au groupe (et pas a la map)
        console.log(map)
        const marker = L.marker(responseData.coord)
            .bindPopup(`Le site de ${responseData.nom} se trouve ici`)
            .openPopup()
            //en l'ajoutant au markerGroup on trigger un event qui fait que ce marker s'affiche sur la map
            .addTo(markerGroup)
        map.flyTo(responseData.coord, 6)

        console.log('Success', responseData)
    }).catch((err) => {
        console.error("Error !!!", err)
    })
})


function displayInfoSite(site) {
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

    // const cardPrevious2 = document.getElementById("card2")
    // if (cardPrevious2) {
    //     cardPrevious2.remove()
    // }
    // const card2 = document.createElement("div")
    // card2.classList.add("card", "col", "raw-mb-8")
    // card2.setAttribute("id", "card2")
    // card2.innerHTML = `
    //     <div class="card-body">
    //         <h5 class="card-title">Ajouter un commentaire</h5>
    //         <form method="post">
    //             <div class="form-group">
    //                 <label hidden name = "name"></label>
    //                 <input type = "pseudo" class="form-control" name="pseudo" placeholder="Rentrez votre pseudo">
    //                 <input hidden name="lieu" value="${site.nom}"/>
    //                 <input type = "contenu_commentaire" class="form-control"  name = "contenu_commentaire"  placeholder="Rédigez votre commentaire">
    //                 <button id = "boutonR" type="submit" class="btn btn-success btn-sm">Publier</button>
    //             </div>
    //         </form>
    //     </div>
    // `

    document.getElementById("displayInfoSite").appendChild(card)
    // document.getElementById("displayInfoSite").appendChild(card2)


    const commentprevious = document.getElementById("commentsCard")
    if (commentprevious) {
        commentprevious.remove()
    }
    const comments = site.comments
    if (comments.length > 0) {
        const commentsCard = document.createElement("div")
        commentsCard.classList.add("card", "col", "raw-mb-8")
        commentsCard.setAttribute("id", "commentsCard")
        commentsCard.innerHTML = `
        <div class="card-body">
            <div class="card-body">
                <h5 class="card-title">Commentaires</h5>
                <ul class="list-group">
                    ${comments.map(comment => `<li class="list-group-item">${comment}</li>`).join('')}
                </ul>
            </div>
        `
        document.getElementById("displayInfoSite").appendChild(commentsCard)
    }



    return card
}
