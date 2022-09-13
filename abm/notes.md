

Will ich das ganze hier Objektorientiert angehen? Ich könnte jeden Akteur als Objekt betrachten, mit assesment und peers. Ich frage mich aber auch schon, ob das Programm dann schnell läuft, oder ob es sich noch irgendwie optimieren lässt.

Große Frage: Wie programmiere ich die Zeitschritte optimal?

Ich will:

- update the assesment of every agent to their observation and the mean of their peers
- update the peers of every agent

Dabei frage ich mich, ob ich die peers von jedem agent schneller finden kann als, indem ich jedes mal jeden anderen Akteur betrachte. (Das ist wichtig, weil die Simulationen sonst lange dauern)

Das ginge, wenn ich die Akteure in einer Liste speichere, die nach ihrem assesment sortiert ist. Dann muss ich mich nur vom gegenwärtigen Akteur nach links und rechts vortasten und kann aufhören, sobald ich zwei finde, die weiter weg sind als epsilon. Ich müsste also die Liste sortieren, nachdem ich die assesments geupdated habe. Könnte sein, dass ich dabei ein paar Schritte spare.

Ich programmiere es jetzt erstmal brute force und wenn ich Geschwindigkeitsprobleme kriege, probier ich die Version.