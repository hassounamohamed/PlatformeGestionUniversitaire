# Script PowerShell pour importer les données via l'API REST
$baseUrl = "http://127.0.0.1:8003"

Write-Host "🚀 Importation des données de référence via API..." -ForegroundColor Cyan

# 1. Importer les salles
Write-Host "`n📍 Importation des salles..." -ForegroundColor Yellow
$salles = @(
    @{numero="LI 03"; capacite=30; type="Laboratoire"},
    @{numero="LI 05"; capacite=30; type="Laboratoire"},
    @{numero="LI 06"; capacite=30; type="Laboratoire"},
    @{numero="LI 07"; capacite=30; type="Laboratoire"},
    @{numero="LG 01"; capacite=30; type="Laboratoire"},
    @{numero="LG 04"; capacite=30; type="Laboratoire"},
    @{numero="SI 01"; capacite=40; type="Salle"},
    @{numero="SI 03"; capacite=40; type="Salle"},
    @{numero="SI 04"; capacite=40; type="Salle"},
    @{numero="SI 09"; capacite=40; type="Salle"},
    @{numero="AMPHI"; capacite=100; type="Amphithéâtre"}
)

$sallesCreated = 0
foreach ($salle in $salles) {
    try {
        $body = $salle | ConvertTo-Json
        Invoke-RestMethod -Uri "$baseUrl/salles" -Method Post -Body $body -ContentType "application/json; charset=utf-8" | Out-Null
        $sallesCreated++
        Write-Host "  ✓ Salle $($salle.numero) créée" -ForegroundColor Green
    } catch {
        Write-Host "  ⚠ Salle $($salle.numero) existe déjà" -ForegroundColor DarkYellow
    }
}
Write-Host "✅ $sallesCreated salles créées" -ForegroundColor Green

# 2. Importer les enseignants
Write-Host "`n👨‍🏫 Importation des enseignants..." -ForegroundColor Yellow
$enseignants = @(
    @{nom="Sarra Jemli"; email="sarra.jemli@iset.tn"},
    @{nom="Wafa Zarroug"; email="wafa.zarroug@iset.tn"},
    @{nom="Houda Najjari"; email="houda.najjari@iset.tn"},
    @{nom="Yousra Ghaouar"; email="yousra.ghaouar@iset.tn"},
    @{nom="Daoud Salah"; email="daoud.salah@iset.tn"},
    @{nom="Ibrahim Chrait"; email="ibrahim.chrait@iset.tn"},
    @{nom="Fadwa Touati"; email="fadwa.touati@iset.tn"},
    @{nom="Taher Ben Youssef"; email="taher.benyoussef@iset.tn"},
    @{nom="Taheya Baccari"; email="taheya.baccari@iset.tn"},
    @{nom="Taha Sfaya"; email="taha.sfaya@iset.tn"},
    @{nom="Mohamed Mbarki"; email="mohamed.mbarki@iset.tn"},
    @{nom="Soufiene B.M"; email="soufiene.bm@iset.tn"},
    @{nom="Ebtihal Hadfi"; email="ebtihal.hadfi@iset.tn"},
    @{nom="Haifa Touati"; email="haifa.touati@iset.tn"},
    @{nom="Bilel Chraigui"; email="bilel.chraigui@iset.tn"},
    @{nom="Dzirya Arfaoui"; email="dzirya.arfaoui@iset.tn"},
    @{nom="Haithem Hafsi"; email="haithem.hafsi@iset.tn"},
    @{nom="Haifa Dguechi"; email="haifa.dguechi@iset.tn"},
    @{nom="Hamed Benneji"; email="hamed.benneji@iset.tn"},
    @{nom="Mariem Jeridi"; email="mariem.jeridi@iset.tn"},
    @{nom="Ibtikhar Chetoui"; email="ibtikhar.chetoui@iset.tn"},
    @{nom="Takwa Omrani"; email="takwa.omrani@iset.tn"},
    @{nom="Ebtihal Hedfi"; email="ebtihal.hedfi@iset.tn"}
)

$enseignantsCreated = 0
foreach ($enseignant in $enseignants) {
    try {
        $body = $enseignant | ConvertTo-Json
        Invoke-RestMethod -Uri "$baseUrl/enseignants" -Method Post -Body $body -ContentType "application/json; charset=utf-8" | Out-Null
        $enseignantsCreated++
        Write-Host "  ✓ $($enseignant.nom) créé(e)" -ForegroundColor Green
    } catch {
        Write-Host "  ⚠ $($enseignant.nom) existe déjà" -ForegroundColor DarkYellow
    }
}
Write-Host "✅ $enseignantsCreated enseignants créés" -ForegroundColor Green

# 3. Importer les matières
Write-Host "`n📚 Importation des matières..." -ForegroundColor Yellow
$matieres = @(
    "Développement Web et Multimédia I",
    "Atelier Développement Web et Multimédia I",
    "Atelier Programmation",
    "Atelier Mathématiques",
    "Atelier Systèmes Logiques",
    "Business Culture",
    "Architecture des Ordinateurs",
    "English for Computing 1",
    "Algorithmique & Programmation 1",
    "Bureautique",
    "Mathématique Appliquée",
    "Technique d'expression 1",
    "2CN",
    "Administration Systèmes",
    "LPIC1",
    "Communication en entreprise",
    "Bases de Données",
    "Atelier Bases de Données",
    "Atelier Programmation Objet",
    "Réseaux Locaux & TCP/IP",
    "Droit de l'Informatique & Propriétés",
    "High Tech English",
    "Cybersecurity Essentials",
    "Programmation Objet",
    "Modélisation Objet (UML2)",
    "Outils de Développement Collaboratif",
    "Programmation Python Avancée",
    "Atelier Développement Web côté Serveur",
    "Atelier Framework côté Client"
)

$matieresCreated = 0
foreach ($nom in $matieres) {
    try {
        $code = ($nom -replace '\s+', '_').Substring(0, [Math]::Min(10, $nom.Length)).ToUpper()
        $body = @{nom=$nom; code=$code; credits=3} | ConvertTo-Json
        Invoke-RestMethod -Uri "$baseUrl/matieres" -Method Post -Body $body -ContentType "application/json; charset=utf-8" | Out-Null
        $matieresCreated++
        Write-Host "  ✓ $nom créée" -ForegroundColor Green
    } catch {
        Write-Host "  ⚠ $nom existe déjà" -ForegroundColor DarkYellow
    }
}
Write-Host "✅ $matieresCreated matières créées" -ForegroundColor Green

Write-Host "`n🎉 Importation terminée!" -ForegroundColor Cyan
