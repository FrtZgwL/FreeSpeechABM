
# Überlegungen zu Optimierung und Objektorientierung

Will ich das ganze hier Objektorientiert angehen? Ich könnte jeden Akteur als Objekt betrachten, mit assesment und peers. Ich frage mich aber auch schon, ob das Programm dann schnell läuft, oder ob es sich noch irgendwie optimieren lässt.

Große Frage: Wie programmiere ich die Zeitschritte optimal?

Ich will:

- update the assesment of every agent to their observation and the mean of their peers
- update the peers of every agent

Dabei frage ich mich, ob ich die peers von jedem agent schneller finden kann als, indem ich jedes mal jeden anderen Akteur betrachte. (Das ist wichtig, weil die Simulationen sonst lange dauern)

Das ginge, wenn ich die Akteure in einer Liste speichere, die nach ihrem assesment sortiert ist. Dann muss ich mich nur vom gegenwärtigen Akteur nach links und rechts vortasten und kann aufhören, sobald ich zwei finde, die weiter weg sind als epsilon. Ich müsste also die Liste sortieren, nachdem ich die assesments geupdated habe. Könnte sein, dass ich dabei ein paar Schritte spare.

Ich programmiere es jetzt erstmal brute force und wenn ich Geschwindigkeitsprobleme kriege, probier ich die Version.

# Wieso konvergiert das innerhalb von 2-3 Zeitschritten

Vielleicht hängt es damit zusammen, dass ich tau Werte nahe 1 oder 0 genommen habe und die Normalverteilung ab 1 oder 0 abschneide.

Irgendwie sind die Daten hier einfach nur Chaos. Weiß nicht, ob das an einem Programmierfehler meinerseits liegt, oder ob das Hegselmann-Krause Modell einfach so ist. __Nächste Schritte:__ Hegeselmann Krause Paper checken; schauen, ob ich deren Daten reproduzieren kann.

# Ideen

Ich baue manche malicious actors ein

Ich teste unterschiedliche Formen von Zensur: 

- social silencing: niemand darf kommunizieren, wenn in bestimmter Range, die weit entfernt von der Mehr heit ist
- state censorship: niemand darf in einer bestimmten Range kommunizieren

Auch beachten: Bei Hegselmann-Krause variiert alpha je nach Akteurgruppe. Sie differenzieren zwischen truth seekers und non-truth-seekers.

" Another view could be to look at as a parameter that can be influenced by intervention. Under such a view, one might start thinking about efficient truth proliferation policies: Which agents, holding what views, should have their attractions to truth modulated in order that all or at least a significant part of a society believes the truth? What if there is time pressure? What to do if the social exchange process has a network structure with primarily local interactions? (Hegselmann-Krause, 242)

# Implementierung von Zensur

1. staatliche zensur: für eine bestimmte range: akteure ignorieren die Meinungen der anderen, wenn sie in diese range fallen
2. social silencing: akteure haben eine fringe-meinung, wenn sie einen bestimmten Abstand zur durchschnittlichen Meinung aller haben
    1. alle, die keine fringe Meinung haben, ignorieren diejenigen mit fringe-Meinungen
    2. wie oben + alle mit fringe Meinungen ignorieren diejenigen ohne fringe Meinungen

# Beobachtungen

Werte in diesem Bereich geben recht schöne Ergebnisse:

Konvergenz:

    n = 30
    epsilon = .2
    alpha = .97
    noise = .1
    tau = .4
    max_time = 20

    n = 40
    epsilon = .2
    alpha = .95
    noise = .2
    tau = .4
    max_time = 20

Polarisierung:

    n = 40
    epsilon = .1
    alpha = .98
    noise = .2
    tau = .4
    max_time = 20

Chaos:

    n = 40
    epsilon = .1
    alpha = .4
    noise = .2
    tau = .4
    max_time = 20

Wenn sie sich besonders gut zuhören, polarisieren sie manchmal

alpha sollte eher hoch sein, sonst nur chaos

# Was für ein Modell?

Will ich ein Modell programmieren, das man dann runterladen und mit dem man herumspielen kann? Oder will ich es nur implementieren, spannende Graphen ausspucken und darüber schreiben?

Wahrscheinlich ersteres, schließlich ist der Deal, dass wir alleine für das Modell bewertet werden.

# Fragen

- warum hat es Auswirkungen auf Akteure, die im Bereich .5-1 glauben, wenn ich 0-.2 zensiere?