# Modèles JSON-LD

Remplace chaque `{{…}}` par une information vraie et visible, ou laisse
`{{à compléter}}` et signale-le. Supprime les propriétés sans valeur plutôt
que d'en inventer une. Un seul bloc `@graph` par page évite les doublons.

## Organisation + site (toutes les pages)

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "{{https://www.site.fr}}/#organisation",
      "name": "{{Nom de la marque}}",
      "url": "{{https://www.site.fr}}/",
      "logo": "{{https://www.site.fr/logo.png}}",
      "description": "{{Une phrase : ce que fait la marque, pour qui}}",
      "sameAs": [
        "{{https://www.linkedin.com/company/…}}",
        "{{https://www.wikidata.org/wiki/Q…}}",
        "{{https://www.youtube.com/@…}}"
      ]
    },
    {
      "@type": "WebSite",
      "@id": "{{https://www.site.fr}}/#site",
      "url": "{{https://www.site.fr}}/",
      "name": "{{Nom du site}}",
      "inLanguage": "fr-FR",
      "publisher": { "@id": "{{https://www.site.fr}}/#organisation" }
    }
  ]
}
```

## Article + auteur

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "{{H1 de la page, 110 caractères max}}",
      "description": "{{meta description}}",
      "datePublished": "{{2026-03-14}}",
      "dateModified": "{{2026-09-30}}",
      "inLanguage": "fr-FR",
      "mainEntityOfPage": "{{URL de la page}}",
      "image": "{{URL de l'image principale}}",
      "author": { "@id": "{{https://www.site.fr/auteurs/prenom-nom}}#personne" },
      "publisher": { "@id": "{{https://www.site.fr}}/#organisation" }
    },
    {
      "@type": "Person",
      "@id": "{{https://www.site.fr/auteurs/prenom-nom}}#personne",
      "name": "{{Prénom Nom}}",
      "jobTitle": "{{Fonction réelle}}",
      "url": "{{https://www.site.fr/auteurs/prenom-nom}}",
      "worksFor": { "@id": "{{https://www.site.fr}}/#organisation" },
      "sameAs": ["{{https://www.linkedin.com/in/…}}"]
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Accueil", "item": "{{https://www.site.fr}}/" },
        { "@type": "ListItem", "position": 2, "name": "{{Blog}}", "item": "{{https://www.site.fr/blog/}}" },
        { "@type": "ListItem", "position": 3, "name": "{{Titre court}}" }
      ]
    }
  ]
}
```

`dateModified` change seulement quand le contenu change vraiment.

## FAQ (seulement si les questions sont visibles sur la page)

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "{{Question telle qu'affichée}}",
      "acceptedAnswer": { "@type": "Answer", "text": "{{Réponse telle qu'affichée}}" }
    }
  ]
}
```

## Produit ou offre

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "{{Nom du produit}}",
  "description": "{{Description visible}}",
  "brand": { "@type": "Brand", "name": "{{Marque}}" },
  "offers": {
    "@type": "Offer",
    "price": "{{49.00}}",
    "priceCurrency": "EUR",
    "availability": "https://schema.org/InStock",
    "url": "{{URL de la page}}"
  }
}
```

`aggregateRating` seulement avec de vrais avis, visibles sur la page, et leur
nombre exact.

## Service

```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "{{Nom du service}}",
  "serviceType": "{{Type}}",
  "provider": { "@id": "{{https://www.site.fr}}/#organisation" },
  "areaServed": [{ "@type": "Country", "name": "France" }],
  "description": "{{Ce que comprend le service}}"
}
```

## Commerce local

```json
{
  "@context": "https://schema.org",
  "@type": "{{Sous-type précis : Dentist, Plumber, Restaurant, AccountingService…}}",
  "name": "{{Nom exact, identique à la fiche Google}}",
  "url": "{{https://www.site.fr/}}",
  "telephone": "{{+33 …}}",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "{{Rue}}",
    "postalCode": "{{75011}}",
    "addressLocality": "{{Paris}}",
    "addressCountry": "FR"
  },
  "openingHoursSpecification": [
    { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "{{09:00}}", "closes": "{{18:00}}" }
  ],
  "sameAs": ["{{URL de la fiche Google}}", "{{Pages Jaunes}}"]
}
```

Nom, adresse et téléphone identiques partout (site, fiche Google,
annuaires).
