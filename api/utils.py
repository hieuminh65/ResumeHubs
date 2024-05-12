def clean_bullet_points(bullet_points):
    bullet_points = bullet_points.split("\n")
    for i in range(len(bullet_points)):
        for letter in bullet_points[i]:
            if letter.isalpha():
                bullet_points[i] = bullet_points[i][bullet_points[i].index(letter):]
                break
    return bullet_points