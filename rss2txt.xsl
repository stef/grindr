<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"><xsl:output method="text" /><xsl:template match="rss/channel">Feed Title: <xsl:value-of select="title" /><xsl:apply-templates select="item" /></xsl:template><xsl:template match="item">
------------------------------
T: <xsl:value-of select="title" />
D: <xsl:value-of select="pubDate" /> 
A: <xsl:value-of select="author" /> 
B: <xsl:value-of select="description" /></xsl:template></xsl:stylesheet>
