
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
% \AtBeginDocument{\markright{\MyTitle \hfill \today \vspace{-5em}}}
\AtBeginDocument{
	\begin{titlepage}
		\thispagestyle{empty}

		{\noindent\Large \today \hfill LMU Munich\\}
		Semester of Summer '22 \hfill Faculty for Philosophy,\\
		Words: 2360 of 6000 \hfill Theory of Science\\
		\raggedleft and Study of Religion
		
		
		\vfill
		\begin{center}
			\noindent \textbf{{\Huge Simulating free speech\\}}
			\vspace{.5em}
			{\Large An agent based modeling approach}
		\end{center}
		
		\vfill

		\begin{center}
			{\noindent\Large PD Dr. habil. Jürgen Landes\\}
			Module: P3 Analysis, reflection and critique of\\ 
			basic problems in theoretical philosophy\\
			Seminar: Social Epistemology

			\vspace{3em}

			{\noindent \Large Cedric Tonye-Djon\\}
			Master: Theoretical Philosophy\\
			Student Number: 12387354\\
			\href{mailto:cedric.tonyedjon@gmail.com}{cedric.tonyedjon@gmail.com}
			%cedric.tonyedjon@gmail.com
		\end{center}
		
	\end{titlepage}

	\tableofcontents
	\clearpage
}
%\setcounter{secnumdepth}{0} % nur, wenn ich keine Überschriftenzählung will


% \AtBeginDocument{
% 	\begin{titlepage}
% 		\thispagestyle{empty}

% 		{\noindent\Large \today \hfill LMU München\\}
% 		Sommersemester \hfill Lehrstuhl für Theoretische Philosophie
% 		\vfill
% 		%\begin{center}
% 			\textsf{{\Huge To what extent is ``objectivity'' reducible?\\}}
% 			% \vspace{.5em}
% 			% {\Large Subtitle}}
% 		%\end{center}
		
% 		\vfill
% 		{\noindent\Large Dr. phil. habil. Alexander Reutlinger \hfill Cedric Tonye-Djon\\}
% 		{P5: Spezialprobleme der analytischen Philosophie \hfill Matrikelnummer 12387354\\}
% 		Scientific Objectivity \hfill cedrictd.ctd@gmail.com
% 	\end{titlepage}

% 	\tableofcontents
% 	\clearpage
% }
