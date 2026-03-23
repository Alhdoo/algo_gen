# Rapport Loan Titouan


```
def best_of_random_solver_section(instance: InstanceData) -> list[int]:
    iterations: int = 100_000

    current = random_solver(instance)
    current_score = tour_distance_km(instance.cities, current, instance.instance_id)

    best = current.copy()
    best_score = current_score

    n = len(current)

    for _ in range(iterations):
        s = current.copy()

        i, j = sorted(random.sample(range(1, n - 1), 2))
        section = s[i:j]

        random.shuffle(section)
        s[i:j] = section

        score = tour_distance_km(instance.cities, s, instance.instance_id)

        print(best_score, current_score, score)

        best_scores.append(best_score)
        current_scores.append(current_score)

        if score < current_score or (random.random() < 0.001 and score - current_score < 100):
            current = s
            current_score = score

        if score < best_score:
            best = s
            best_score = score

    return best
```

Explication:
1. L'algorithme part de la liste originelle et applique un premier shuffle.
2. Il lance ensuite les itérations.
3. À chaque itération, on choisit 2 indices aléatoires.
4. On mélange le segment entre ces deux indices.
5. On recalcule le score de la nouvelle solution.
6. On remplace la solution courante si elle est meilleure.
7. Pour favoriser l'exploration, on garde parfois une solution moins bonne avec une faible probabilité.

C'est notre propre algorithme qui est décrit ici, que nous avons également effectué quelques tests avec Codex 5.4 High
