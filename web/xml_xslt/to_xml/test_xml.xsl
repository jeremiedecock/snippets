<?xml version="1.0" encoding="UTF-8" ?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

    <xsl:output method="xml" indent="yes" />

    <xsl:template match="/">
        <carnet>
            <xsl:for-each select="/carnet/nom">
                <nom>
                    <prenom> <xsl:value-of select="@prenom" /> </prenom>
                    <prenom2> <xsl:value-of select="@prenom2" /> </prenom2>
                    <famille> <xsl:value-of select="@famille" /> </famille>
                </nom>
            </xsl:for-each>
        </carnet>
    </xsl:template>

</xsl:stylesheet>
