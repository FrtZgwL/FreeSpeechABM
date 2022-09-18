
% --- Setup Class --- %
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{essay-formal}
\LoadClass[12pt,DIV=10]{scrartcl} % DIV ist für die Seitenränder

% --- KOMA Script Optionen --- %
\usepackage[onehalfspacing]{setspace}
\KOMAoptions{headinclude=true,titlepage=false,headsepline=true}
\recalctypearea

% --- Weitere Packete --- %
\usepackage[english]{babel} % Damit Datum, "Inhaltsverzeichnis, etc. die richtige Sprache haben"
\usepackage{blindtext} % zum Gestalten
\usepackage{enumitem} % Um für Definitionen die linke Margin bei Enumerations zu entfernen

% Ziemlich ziemlich nice Schrift, cooles Projekt
% Seit 1995 in entwicklung, offen und frei, mit Mathe, Kursiv, Fett, Smallcaps
% STIX (Science and Technical Inforamation Exchange)
\usepackage[T1]{fontenc}
\usepackage{stix2}

% \usepackage{xcolor}
\usepackage{hyperref}
% \hypersetup{
% 	% linkbordercolor = {white} => This works but not everything is that kind of link!
% }

%\pdftitle	= {\@title} TODO: one day: einheitliches System, Autor, etc. an einer Stelle definieren
%\pdfsubject	= {\@subject}
%\pdfauthor	= {\@author}

% --- Meine Befehle --- %
\newenvironment{definitions}
	{\begin{description}\setlist[enumerate]{leftmargin=*}}
	{\end{description}}
\newcommand{\definition}[2]{
	\begin{definitions}
		\item[#1] #2
	\end{definitions}
}

% --- Stil --- %
\pagestyle{headings}

% \addtokomafont{disposition}{\rmfamily\itshape} % This would be awesome for handouts!
\addtokomafont{disposition}{\rmfamily}

% Kurzer Essay

%\setcounter{secnumdepth}{0} % nur, wenn ich keine Überschriftenzählung will



