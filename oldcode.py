

def init_game(state: dict):
    state.clear()

    player = pygame.sprite.Group()
    player.add(Ship(BOARD_SIZE[0] // 2, BOARD_SIZE[1] // 4 * 3))

    stars = pygame.sprite.Group()
    for _ in range(STAR_COUNT):
        stars.add(Star(randint(0, BOARD_SIZE[0]), randint(0, BOARD_SIZE[1])))

    fuel = pygame.sprite.Group()
    for _ in range(FUEL_COUNT):
        fuel.add(
            Fuel(
                randint(0, BOARD_SIZE[0]),
                randint(0, BOARD_SIZE[1]),
                randint(-50, 50) / 10.0,
                randint(-50, 50) / 10.0,
            )
        )

    rocks = pygame.sprite.Group()
    for _ in range(ROCKS_COUNT):
        rocks.add(
            Rock(
                randint(0, BOARD_SIZE[0]),
                randint(0, BOARD_SIZE[1]),
                randint(-50, 50) / 5.0,
                randint(-50, 50) / 5.0,
            )
        )

    state["sprites"] = {"stars": stars, "rocks": rocks, "fuel": fuel, "player": player}
    state.update({"score": 0, "fuel": 100.0, "max_fuel": 100.0})


def main():
    pygame.init()

    screen = pygame.display.set_mode(SCREEN_SIZE)  # , pygame.FULLSCREEN)
    pygame.display.set_caption("fuel tanker")
    board = pygame.Surface(BOARD_SIZE)
    clock = pygame.time.Clock()

    state = {}
    init_game(state)

    running = True
    while running:
        clock.tick(FPS)
        # quit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                if event.key == pygame.K_r and state.get("game") == "over":
                    init_game(state)

        if running:
            # recomputes
            for group in state["sprites"].values():
                group.update(state, BOARD_SIZE)

            # draws
            board.fill(BG_COLOR)
            for group in state["sprites"].values():
                # group.clear(board, background)
                group.draw(board)

        screen.blit(board, (0, 0))
        # fps
        write(f"{clock.get_fps():.02f} fps", 0, screen)
        # score
        write(f"SCORE: {state['score']}", 1, screen)
        # fuel
        write(f"FUEL: {state['fuel']:.02f}", 2, screen)

        if state.get("game") == "over":
            gameover(screen)

        pygame.display.flip()

    pygame.quit()
