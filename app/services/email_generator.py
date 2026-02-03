def generate_email_content(business_name: str, category: str) -> dict:
    """
    Crée un objet email avec sujet et corps basé sur le business.
    """
    subject = f"Proposition spéciale pour votre {category} : {business_name}"
    
    body = f"""
    <html>
        <body>
            <p>Bonjour {business_name},</p>
            <p>Nous avons une offre spéciale qui pourrait intéresser votre {category}.</p>
            <p>N'hésitez pas à nous contacter pour en savoir plus !</p>
            <p>Bonne journée,</p>
            <p>L'équipe Local Business Finder AI</p>
        </body>
    </html>
    """
    return {"subject": subject, "body": body}
