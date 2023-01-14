# IMC_NET2_SIMP
feedback from Ruben:
Some general remarks:
- Instead of (almost) duplicating the start_chatting function, you could have written a module with functions needed by both client and server.
- Instead of using integer literals for indexing arrays, please think about using constants with a corresponding name. The code will be clearer.

Evaluation:
- Message implementation correct: 25 points
- Handshake implementation also technically correct: 10 points
- Stop and wait: Handling of chat messages ok but after a FIN from the client the server needs to be restarted again (instead of waiting for more incoming connections): 7 points
- Documentation: Report well written. As commented before, the code could have been more clear if constaints instead of integer literals were used for indexing arrays (or using enums for defining operations). 3 points
Points
45 / 50
