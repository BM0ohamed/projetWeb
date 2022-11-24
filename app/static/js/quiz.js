//quand j'ai écrit cette fonction y'avait que moi et dieu qui comprenions, 
//mtn y'a que dieu sah

async function sendInfoServer(url,options) {
    let response = await fetch(url,options)
    if(response.ok){
        let data = await response.json()
        return data
    }
    return null
}

const elementsWithValueToSend = document.querySelectorAll("[data-value-to-send]")

elementsWithValueToSend.forEach(elementWithValueToSend => {
    elementWithValueToSend.addEventListener('click', (e) => {
        // On affiche un loader le temps que ça charge
        const loader = document.createElement("div")
        loader.classList.add("loader")
        document.getElementById("contient_boutons").appendChild(loader)

        // On récupère la valeur du bouton
        const value = elementWithValueToSend.getAttribute("data-value-to-send")
        // On demande au serveur si c'est la bonne réponse
        const response = sendInfoServer("/quiz", {
            method: 'post',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                siteSelected: value
            })
        }).then((res) => {
            // Si on a une réponse on supprime tous les boutons précédents
            elementsWithValueToSend.forEach(e => e.remove())

            // Si c'est un bon site
            if (res.isGoodSite) {
                const successMessage = document.createElement("div")
                successMessage.classList.add("alert", "alert-success")
                successMessage.innerHTML = `
                    <p><i class="tim-icons icon-check-2"></i> Bravo ! ${res.goodSiteIs} était bel et bien le bon site!</p>
                    <a href="/quiz" class="btn btn-primary"><i class="tim-icons icon-refresh-01"></i> Recommencer</a>
                `
                document.getElementById("contient_boutons").appendChild(successMessage)
            }
            // Si c'est un mauvais site
            if (!res.isGoodSite) {
                const failMessage = document.createElement("div")
                failMessage.classList.add("alert", "alert-danger")
                failMessage.innerHTML = `
                    <p> <i class="tim-icons icon-simple-remove"></i> Dommage ! la réponse était : ${res.goodSiteIs}, tu avais sélectionné : ${value}</p>
                    <a href="/quiz" class="btn btn-primary"><i class="tim-icons icon-refresh-01"></i> Recommencer</a>
                `
                document.getElementById("contient_boutons").appendChild(failMessage)
            }
        }).catch((err) => {
            // Si on a un erreur
            console.log(err)
        }).then(() => {
            loader.remove()
        });
    })
})