% Homework document class
% Adam Wilson
% 2017

% preamble
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{homework}[2017/01/13 v0.1 Homework document class]

\LoadClass[letterpaper, 12pt]{article}

\RequirePackage[top=1in,bottom=1in,left=1in,right=1in]{geometry}
\RequirePackage{fancyhdr}
\RequirePackage{xparse}
\RequirePackage{etoolbox}
\RequirePackage{lastpage}

% assignment details
\newcommand*{\@student}{Student Name}
\newcommand*{\@studentid}{}
\newcommand*{\@class}{Class Name}
\newcommand*{\@assignment}{Assignment Name}
\newcommand*{\@duedate}{}
\newcommand*{\@semester}{}
\newcommand*{\@professor}{}

\newcommand*{\student}[1]{\renewcommand{\@student}{#1}}
\newcommand*{\studentid}[1]{\renewcommand{\@studentid}{#1}}
\newcommand*{\class}[1]{\renewcommand{\@class}{#1}}
\newcommand*{\assignment}[1]{\renewcommand{\@assignment}{#1}}
\newcommand*{\due}[1]{\renewcommand{\@duedate}{#1}}
\newcommand*{\semester}[1]{\renewcommand{\@semester}{#1}}
\newcommand*{\professor}[1]{\renewcommand{\@professor}{#1}}

% set header/footer
\setlength{\headheight}{15pt}
\lhead{\@student}\chead{\@assignment}\rhead{\@class}
\lfoot{}\cfoot{\thepage~of~\pageref{LastPage}}\rfoot{}
\pagestyle{fancy}

% title page
\renewcommand{\maketitle}{%
\thispagestyle{empty}
\begin{center}~

\vspace{2.5cm}\Huge \textbf{\@assignment}

\vspace{0.5cm}
\large \@class

\small
\ifdefempty{\@duedate}{}{Due \@duedate}

\ifdefempty{\@professor}{}{Prof. \@professor}

\ifdefempty{\@semester}{}{\@semester}

\vfill
\normalsize
\textbf{\@student \ifdefempty{\@studentid}{}{\\\@studentid}}

\end{center}
\cleardoublepage
\setcounter{page}{1}}

% problem counters
\newcounter{ProblemNumber}
\newcounter{SubProblemNumber}[ProblemNumber]

\renewcommand{\theProblemNumber}{\arabic{ProblemNumber}}
\renewcommand{\theSubProblemNumber}{\alph{SubProblemNumber}}

\setlength{\parskip}{10pt}
\setlength{\parindent}{0pt}

%problem command
\ExplSyntaxOn
\NewDocumentEnvironment{problem} { o g }
{%
	\par\noindent
	\IfNoValueTF{#1}{\stepcounter{ProblemNumber}}{}
	\section*{\IfNoValueTF{#1}{Problem~\theProblemNumber}{#1}%
			  \IfNoValueTF{#2}{}{:~#2}}
	\ignorespaces%
}
{}
\ExplSyntaxOff

\newenvironment{statement}%
{}%
{\par%\vspace{2mm}
\noindent\hfil\rule{0.75\textwidth}{.4pt}\hfil%
\par%\vspace{2mm}
}