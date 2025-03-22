from chess.State import InitialiseState, StartScreenState


def main():
    InitialiseState.initialise()

    running = True
    currentState = StartScreenState
    while running:
        stateDict: dict = currentState.run()
        if stateDict["quit"]:
            running = False

        currentState = stateDict["nextState"]


if __name__ == "__main__":
    main()
