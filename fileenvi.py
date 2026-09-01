from deepagents.backends import StateBackend


# Create an environment/backend
backend = StateBackend()


# Write something into the environment
backend.write(
    "/notes.txt",
    "This is my first file stored in the environment."
)


# Read it back
content = backend.read("/notes.txt")

print("CONTENT STORED IN ENVIRONMENT:")
print(content)