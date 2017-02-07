% Homework document class
% Adam Wilson
% 2017

% preamble
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{homework}[2017/01/13 v0.1 Homework document class]

\LoadClass[en-US, letterpaper, 11pt]{article}

\RequirePackage[english]{babel}
\RequirePackage[utf8]{inputenc}
\RequirePackage[top=1in,bottom=1in,left=1in,right=1in]{geometry}
\RequirePackage{fancyhdr}
\RequirePackage{xparse}
\RequirePackage{etoolbox}
\RequirePackage{lastpage}
\RequirePackage[english, calc, useregional, datesep=/]{datetime2}

\DTMnewdatestyle{DOWMonthDay}{%
% ##1 = year
% ##2 = month
% ##3 = day
% ##4 = dow
\renewcommand*{\DTMdisplaydate}[4]{% 
\DTMenglishweekdayname{##4}~\DTMenglishmonthname{##2}
% ordinals function from the language pack doesn't seem to be working, so I recreated it below
\number##3
\textsuperscript{%
\ifcase##3
\or \DTMenglishst
\or \DTMenglishnd
\or \DTMenglishrd
\or \DTMenglishth
\or \DTMenglishth
\or \DTMenglishth
\or \DTMenglishth
\or \DTMenglishth
\or \DTMenglishth
\or \DTMenglishth
\or \DTMenglishth
\or \DTMenglishth
\or \DTMenglishth
\or \DTMenglishth
\or \DTMenglishth
\or \DTMenglishth
\or \DTMenglishth
\or \DTMenglishth
\or \DTMenglishth
\or \DTMenglishth
\or \DTMenglishst
\or \DTMenglishnd
\or \DTMenglishrd
\or \DTMenglishth
\or \DTMenglishth
\or \DTMenglishth
\or \DTMenglishth
\or \DTMenglishth
\or \DTMenglishth
\or \DTMenglishth
\or \DTMenglishst
\fi}}%
\renewcommand*{\DTMDisplaydate}{\DTMdisplaydate}%
}

\DTMsetdatestyle{mdyyyy}

% assignment details
\newcommand*{\@student}{Student Name}
\newcommand*{\@studentid}{}
\newcommand*{\@class}{Class Name}
\newcommand*{\@section}{}
\newcommand*{\@assignment}{Assignment Name}
\newcommand*{\@duedate}{}
\newcommand*{\@semester}{}
\newcommand*{\@year}{}
\newcommand*{\@professor}{}
\newcommand*{\@school}{}

\newcommand*{\student}[1]{\renewcommand{\@student}{#1}}
\newcommand*{\studentid}[1]{\renewcommand{\@studentid}{#1}}
\newcommand*{\class}[2]{\renewcommand{\@class}{#1}\renewcommand{\@section}{#2}}
\newcommand*{\assignment}[1]{\renewcommand{\@assignment}{#1}}
\newcommand*{\due}[1]{\DTMsavedate{duedate}{#1}\renewcommand{\@duedate}{#1}}
\newcommand*{\semester}[2]{\renewcommand{\@semester}{#1}\renewcommand{\@year}{#2}}
\newcommand*{\professor}[1]{\renewcommand{\@professor}{#1}}
\newcommand*{\school}[1]{\renewcommand{\@school}{#1}}

% set header/footer
\setlength{\headheight}{15pt}
\lhead{\@student}\chead{\@assignment}\rhead{\@class}
\lfoot{\@school}\cfoot{\thepage~of~\pageref{LastPage}}\rfoot{\@semester~\@year}
\renewcommand\headrulewidth{0.4pt}
\renewcommand\footrulewidth{0.4pt}
\pagestyle{fancy}

% title page
\renewcommand*{\maketitle}{\coverpage}
\newcommand{\coverpage}{%
\thispagestyle{empty}
\begin{center}~

\vspace{1.0cm}\Huge \textbf{\@assignment}

\vspace{1.5cm}
\normalsize \@class \ifdefempty{\@section}{}{~-~\@section}\\
\ifdefempty{\@semester}{}{~\@semester~\@year\\}
\ifdefempty{\@school}{}{\@school\\}
\ifdefempty{\@professor}{}{Prof. \@professor\\}
\ifdefempty{\@duedate}{}{\DTMsetdatestyle{DOWMonthDay}Due \DTMusedate{duedate}\DTMsetdatestyle{mdyyyy}}

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