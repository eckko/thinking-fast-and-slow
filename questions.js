// Question bank. Add more objects to this array (or generate them with a skill later).
// kind: "mcq" (options + answer index) or "recall" (cue + model answer in "a").
window.QUIZ = {
  id: "thinking-fast-and-slow",
  book: "Thinking, Fast and Slow",
  questions: [
    {
      id: "c09-1", unit: "Chapter 9", unitTitle: "Answering an Easier Question",
      section: "Place in the argument", kind: "mcq",
      q: "Why does the author place “Answering an Easier Question” at the end of Part 1?",
      options: [
        "It is a standalone chapter on perception, placed last because it is the shortest.",
        "It shows that System 2 is usually in charge, which settles the debate about the two systems.",
        "It combines the pieces built earlier in Part 1 into substitution, the engine of heuristics, and closes with a list of System 1’s characteristics.",
        "It reviews Part 1’s experiments and states the book’s recommendations for decision-makers."
      ],
      answer: 2,
      explain: "Chapter 9 is the culmination of Part 1: basic assessments, the mental shotgun, intensity matching, a lazy System 2 and WYSIATI yield substitution. Its closing list doubles as an index of Part 1 and a preview of Part 4."
    },
    {
      id: "c09-2", unit: "Chapter 9", unitTitle: "Answering an Easier Question",
      section: "Substituting Questions", kind: "mcq",
      q: "What is the difference between the target question and the heuristic question?",
      options: [
        "The target question is the assessment you intend to produce; the heuristic question is the simpler question you answer instead.",
        "The target question is answered by System 2 and the heuristic question by System 1, and both are answered every time.",
        "The heuristic question is the hard one the experimenter asks; the target question is the one the participant invents.",
        "The target question is always about probability; the heuristic question is always about feelings."
      ],
      answer: 0,
      explain: "Substitution: “If a satisfactory answer to a hard question is not found quickly, System 1 will find a related question that is easier and will answer it.”"
    },
    {
      id: "c15-1", unit: "Chapter 15", unitTitle: "Linda: Less is More",
      section: "Opening", kind: "recall",
      q: "What is the conjunction fallacy, and why does the Linda problem demonstrate it?",
      a: "Judging a conjunction of two events as more probable than one of them in a direct comparison. Linda fits “feminist” better, so “feminist bank teller” was ranked more likely than “bank teller”, though every feminist bank teller is a bank teller: “When you specify a possible event in greater detail you can only lower its probability.” The problem sets representativeness against logic, and the error stays attractive even when recognised."
    },
    {
      id: "c15-2", unit: "Chapter 15", unitTitle: "Linda: Less is More",
      section: "Less is More, Sometimes Even in Joint Evaluation", kind: "mcq",
      q: "In the conjunction problem, what cut errors from 65% to 25%?",
      options: [
        "Giving participants more time to think.",
        "Asking “How many of the 100 participants…” instead of “What percentage…”.",
        "Showing participants a Venn diagram first.",
        "Using only participants trained in statistics."
      ],
      answer: 1,
      explain: "The frequency representation makes inclusion obvious; “how many?” makes you think of individuals."
    },
    {
      id: "c37-1", unit: "Chapter 37", unitTitle: "Experienced Well-Being",
      section: "Experienced Well-Being", kind: "mcq",
      q: "What did the Gallup-Healthways data show about income and well-being?",
      options: [
        "Experienced well-being and life satisfaction both rise steadily with income.",
        "Neither experienced well-being nor life satisfaction is related to income.",
        "Experienced well-being keeps rising with income, while life satisfaction levels off.",
        "Experienced well-being stops increasing at about $75,000 household income in high-cost areas, while life satisfaction keeps rising."
      ],
      answer: 3,
      explain: "Poverty makes one miserable; riches may enhance life satisfaction but do not (on average) improve experienced well-being. Life evaluation and actual experience “are also different.”"
    }
  ]
};
