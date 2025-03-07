from chess.State import InitialiseState, NewScreenState


def main():
    InitialiseState.initialise()

    running = True
    currentState = NewScreenState
    while running:
        stateDict: dict = currentState.run()
        if stateDict["quit"]:
            running = False

        currentState = stateDict["nextState"]


if __name__ == "__main__":
    main()
