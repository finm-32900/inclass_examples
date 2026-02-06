%%%   Modified from protocol.cls for two-column layout using paracol.
%%%   Original by Danny Awty-Carroll, based on:
%%%%%%%%%%%%%%%%%
% This is altacv.cls (v1.1.3, 30 April 2017) written by
% LianTze Lim (liantze@gmail.com).
%
%% It may be distributed and/or modified under the
%% conditions of the LaTeX Project Public License, either version 1.3
%% of this license or (at your option) any later version.
%% The latest version of this license is in
%%    http://www.latex-project.org/lppl.txt
%% and version 1.3 or later is part of all distributions of LaTeX
%% version 2003/12/01 or later.
%%%%%%%%%%%%%%%%
\NeedsTeXFormat{LaTeX2e}[1995/12/01]
\ProvidesClass{handout2}[2024/01/01 Two-column handout template v0.1]

%% v1.1: Optionally load academicons
\newif\if@academicons
\DeclareOption{academicons}{\@academiconstrue}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{extarticle}}
\ProcessOptions\relax

\LoadClass{extarticle}

\RequirePackage[left=1.5cm,right=1.5cm,top=1cm,bottom=1cm]{geometry}
\RequirePackage{fontawesome}
\RequirePackage{paracol}

%% v1.1: Optionally load academicons
\if@academicons
  %% Patch to make academicons compilable with XeLaTeX
  \ExplSyntaxOn
  \msg_redirect_name:nnn { fontspec } { font-not-found } { none }
  \ExplSyntaxOff
  \RequirePackage{academicons}
  \newfontfamily{\AI}{academicons.ttf}
\fi


\RequirePackage{xcolor}

\colorlet{accent}{blue!90!black}
\colorlet{heading}{black}
\colorlet{titlecolor}{black}
\colorlet{emphasis}{black}
\colorlet{body}{black!80!white}
\newcommand{\itemmarker}{{\small\textbullet}}
\newcommand{\ratingmarker}{\faCircle}

\RequirePackage{tikz}
\usetikzlibrary{arrows}
\RequirePackage[skins]{tcolorbox}
\RequirePackage{enumitem}
\setlist{leftmargin=*,labelsep=0.5em,nosep,itemsep=0.25\baselineskip,after=\vskip0.25\baselineskip}
\setlist[itemize]{label=\itemmarker}
\RequirePackage{graphicx}
\RequirePackage{etoolbox}
\RequirePackage{dashrule}
\RequirePackage{multirow,tabularx}
\RequirePackage{changepage}

\setlength{\parindent}{0pt}
\newlength{\@sidecolwidth}
\setlength{\@sidecolwidth}{4.5cm}
\newcommand{\divider}{\textcolor{body!30}{\hdashrule{\linewidth}{0.6pt}{0.5ex}}\medskip}

% With symmetric geometry, fullwidth is a no-op (header is placed before paracol)
\newenvironment{fullwidth}{}{}


\newcommand{\name}[1]{\def\@name{#1}}
\newcommand{\asof}[1]{\def\@asof{#1}}
\newcommand{\tagline}[1]{\def\@tagline{#1}}
\newcommand{\logo}[2]{\def\@logo{#2}\def\@logodiameter{#1}}

\newcommand{\analyst}[2]{\mbox{\textcolor{emphasis}{#1} \hspace{0.3em}\textcolor{accent}{\faEnvelope}\hspace{0.3em}\textcolor{body}{#2}}}


\newcommand{\docinfo}[1]{\def\@docinfo{#1}}

\newcommand{\makeheader}{%
  \begingroup
    \ifdef{\@logodiameter}{%
      \begin{minipage}[t]{\dimexpr\linewidth-\@logodiameter-1em\relax}%
      \vspace{0pt}%
    }{}%
    \raggedright%
    {\Huge\bfseries\color{titlecolor}\MakeUppercase{\@name}\par}
    \medskip
    {\large\bfseries\color{accent}\@tagline\par}
    \medskip
    {\large\bfseries\color{emphasis}\@asof\par}
    \smallskip
    {\footnotesize\@docinfo\par}
    % \mbox{\tiny\textcolor{body}{Published \today}}
    \ifdef{\@logodiameter}{%
      \end{minipage}\hfill%
      \begin{minipage}[t]{\@logodiameter}%
        \vspace{0pt}%
        \centering
        \includegraphics[width=\@logodiameter]{\@logo}%
      \end{minipage}%
    }{}%
    \par
  \endgroup\smallskip
}

\renewenvironment{quote}{\color{accent}\itshape\large}{\par}

% Simplified \need: just a section heading, no sidebar/marginpar/input
\newcommand{\need}[1]{%
  \bigskip%
	\medskip
  {\color{heading}\LARGE\bfseries\MakeUppercase{#1}}\\[-1ex]%
  {\color{heading}\rule{\linewidth}{2pt}\par}\medskip
}

\newcommand{\protosubsection}[1]{%
  \smallskip%
  {\color{emphasis}\large\bfseries{#1}\par}\medskip
}

\newcommand{\step}[3]{%
  \color{emphasis}{Step }
  {\large\color{emphasis}#1}
  \hfill
  \color{emphasis}{\footnotesize  [Time required #3 minutes]\par}
  \smallskip
  \textbf{\color{accent}{#2} }\par
  \smallskip
}

\newcommand{\warningsigns}[3]{%
  \begin{tabularx}{\linewidth}{@{}p{2em} @{\hspace{1ex}} >{\raggedright\arraybackslash}X@{}}
  \multirow{2}{*}{\Large\color{accent}#1} & \bfseries\textcolor{emphasis}{#2}\\
  & #3
  \end{tabularx}%
  \smallskip
}

\newcommand{\itemtag}[1]{%
  \tikz[baseline]\node[anchor=base,draw=body!30,rounded corners,inner xsep=1ex,inner ysep =0.75ex,text height=1.5ex,text depth=.25ex]{#1};
}

\newcommand{\risk}[2]{%
\textcolor{emphasis}{\textbf{#1}}\hfill
\foreach \x in {1,...,5}{%
  \space{\ifnumgreater{\x}{#2}{\color{body!30}}{\color{accent}}\faCircle}}\par%
}


\newcommand{\protoref}[3]{%
  \smallskip
  \textcolor{emphasis}{\textbf{#1}}\par
  \begin{description}[font=\color{accent},style=multiline,leftmargin=1.25em]
  \item[\faSpinner] #2
  \item[\small\faSpinner] #3
  \end{description}
%   \medskip
}

\newenvironment{protocolumn}[1]{\begin{minipage}[t]{#1}\raggedright}{\end{minipage}}

\RequirePackage[utf8]{inputenc}
\RequirePackage[backend=biber,style=authoryear,sorting=ydnt]{biblatex}
%% For removing numbering entirely when using a numeric style
\setlength{\bibhang}{1em}
\DeclareFieldFormat{labelnumberwidth}{\makebox[\bibhang][l]{\itemmarker}}
\setlength{\biblabelsep}{0pt}
\defbibheading{pubtype}{\protosubsection{#1}}
\renewcommand{\bibsetup}{\vspace*{-\baselineskip}}
\AtEveryBibitem{\makebox[\bibhang][l]{\itemmarker}}
\setlength{\bibitemsep}{0.25\baselineskip}

\AtBeginDocument{%
  \pagestyle{empty}
  \color{body}
  \raggedright
}
