// Import necessary libraries
import { AppBar, Box, Button, Grid, LinearProgress, Paper, TextField, Toolbar, Typography } from '@mui/material';
import { motion } from 'framer-motion';
import React, { useState } from 'react';

const HaskellITS = () => {
  const [code, setCode] = useState('');
  const [progress, setProgress] = useState(0);
  const [output, setOutput] = useState('');
  const [currentProblem, setCurrentProblem] = useState('');
  const [showHints, setShowHints] = useState(false);
  const [showSolution, setShowSolution] = useState(false);

  const problems = {
    "Writing Recursive Functions": {
      description: `Implement a recursive function fib :: Integer -> Integer that computes the n-th Fibonacci number.`,
      hints: [
        "Define the base cases for n = 0 and n = 1.",
        "Combine fib(n-1) and fib(n-2) for recursion."
      ],
      solution: `fib :: Integer -> Integer\nfib 0 = 0\nfib 1 = 1\nfib n = fib (n-1) + fib (n-2)`
    },
    "Using Higher-Order Functions": {
      description: `Use map, filter, and reduce to process lists.`,
      hints: [
        "Use map to transform each element in a list.",
        "Use filter to select even numbers from a list.",
        "Use reduce to calculate the sum of a list."
      ],
      solution: `let numbers = [1, 2, 3, 4]\nlet evens = filter even numbers\nlet doubled = map (*2) evens\nlet sum = foldr (+) 0 doubled`
    },
    "Understanding Type Systems and Data Types": {
      description: `Define custom data types and explore polymorphism in Haskell.`,
      hints: [
        "Define a data type using the data keyword.",
        "Implement typeclasses and instances.",
        "Use polymorphism in function signatures."
      ],
      solution: `data Shape = Circle Float | Rectangle Float Float\narea :: Shape -> Float\narea (Circle r) = pi * r * r\narea (Rectangle w h) = w * h`
    },
  };

  const syntaxBasics = `-- Haskell Syntax Basics

-- Initializing Variables
-- Variables in Haskell are immutable and can be defined using the let or where keyword.

-- Using let in a local context:
let x = 10
let y = 20
let sum = x + y  -- sum will be 30

-- Using where in function definitions:
calculateArea radius = pi * radius * radius
  where pi = 3.14159

-- Global definitions (not scoped to a block):
myConstant :: Int
myConstant = 42

-- Define a function
-- Functions in Haskell are defined using a name, type signature, and implementation.
add :: Int -> Int -> Int
add x y = x + y

-- Use recursion
-- Recursion is fundamental in Haskell and is often used instead of loops.
factorial :: Integer -> Integer
factorial 0 = 1
factorial n = n * factorial (n - 1)

-- Use higher-order functions
-- Higher-order functions take other functions as arguments or return them as results.
let numbers = [1, 2, 3]
let squares = map (\\x -> x * x) numbers
let evens = filter even numbers
let sumOfSquares = foldr (+) 0 squares

-- Define a data type
-- Haskell allows defining custom data types with the data keyword.
data Shape = Circle Float | Rectangle Float Float

-- Pattern match to handle different cases for custom data types.
area :: Shape -> Float
area (Circle r) = pi * r * r
area (Rectangle w h) = w * h

-- Use lists
-- Lists are a fundamental data structure in Haskell, and they are immutable.
let emptyList = []
let myList = [1, 2, 3]
let listHead = head myList
let listTail = tail myList
let concatenatedList = myList ++ [4, 5]

-- Lambda expressions
-- Lambdas are anonymous functions defined using the \\ syntax.
let addOne = \\x -> x + 1
let result = addOne 5  -- Result: 6

-- List comprehensions
-- A concise way to generate lists based on existing ones.
let squaresOfEvens = [x * x | x <- [1..10], even x]

-- Guards
-- A clean way to define multiple cases in a function.
classifyNumber :: Int -> String
classifyNumber n
  | n < 0 = "Negative"
  | n == 0 = "Zero"
  | otherwise = "Positive"

-- Case expressions
-- An alternative to guards for pattern matching.
describeList :: [a] -> String
describeList xs = case xs of
  [] -> "Empty list"
  [x] -> "Singleton list"
  _ -> "A longer list"

-- Typeclasses
-- Haskell uses typeclasses to define shared behavior for types.
class Eq a where
  (==) :: a -> a -> Bool

-- An example of using the built-in Eq typeclass for comparison.
instance Eq Bool where
  True == True = True
  False == False = True
  _ == _ = False
`;



  const handleRunCode = () => {
    try {
      // Mock evaluation
      if (currentProblem === "Writing Recursive Functions" && code.includes("fib")) {
        setOutput("Success! Recursive function implemented.");
        setProgress((prev) => Math.min(prev + 20, 100));
      } else if (currentProblem === "Using Higher-Order Functions" && code.includes("map")) {
        setOutput("Success! Higher-order function used.");
        setProgress((prev) => Math.min(prev + 20, 100));
      } else {
        setOutput("Error: Code does not meet the task requirements.");
      }
    } catch (error) {
      setOutput("Runtime Error: " + error.message);
    }
  };

  const selectProblem = (problemKey) => {
    setCurrentProblem(problemKey);
    setCode('');
    setOutput('');
    setShowHints(false);
    setShowSolution(false);
  };

  return (
    <Box sx={{ height: '100vh', backgroundColor: '#f5f5f5' }}>
      {/* Header Section */}
      <AppBar position="static" color="primary">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            Mastering Haskell ITS
          </Typography>
          <Button color="inherit">Login</Button>
        </Toolbar>
      </AppBar>

      {/* Syntax Basics Section */}
      <Grid container spacing={2} sx={{ p: 3 }}>
        <Grid item xs={12}>
          <Paper elevation={3} sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Haskell Syntax Basics
            </Typography>
            <TextField
              multiline
              rows={10}
              fullWidth
              value={syntaxBasics}
              variant="outlined"
              sx={{ fontFamily: 'monospace' }}
              InputProps={{ readOnly: true }}
            />
          </Paper>
        </Grid>
      </Grid>

      {/* Main Content */}
      <Grid container spacing={2} sx={{ p: 3 }}>
        {/* Problem Selector */}
        <Grid item xs={12} md={4}>
          <Paper elevation={3} sx={{ p: 2, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              Select a Problem
            </Typography>
            {Object.keys(problems).map((key) => (
              <Button
                key={key}
                variant="outlined"
                color="primary"
                fullWidth
                sx={{ mb: 1 }}
                onClick={() => selectProblem(key)}
              >
                {key}
              </Button>
            ))}
          </Paper>
        </Grid>

        {/* Problem Description and Code Editor */}
        <Grid item xs={12} md={8}>
          <motion.div
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
          >
            <Paper elevation={3} sx={{ p: 2, height: '100%' }}>
              <Typography variant="h6" gutterBottom>
                Problem Description
              </Typography>
              {currentProblem ? (
                <>
                  <Typography variant="body1" gutterBottom>
                    {problems[currentProblem].description}
                  </Typography>
                  <Button
                    variant="outlined"
                    color="secondary"
                    onClick={() => setShowHints(!showHints)}
                    sx={{ mb: 2 }}
                  >
                    {showHints ? "Hide Hints" : "Show Hints"}
                  </Button>
                  {showHints && (
                    <ul>
                      {problems[currentProblem].hints.map((hint, index) => (
                        <li key={index}>{hint}</li>
                      ))}
                    </ul>
                  )}
                  <Button
                    variant="outlined"
                    color="secondary"
                    onClick={() => setShowSolution(!showSolution)}
                    sx={{ mb: 2, ml: 1 }}
                  >
                    {showSolution ? "Hide Solution" : "Show Solution"}
                  </Button>
                  {showSolution && (
                    <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
                      {problems[currentProblem].solution}
                    </Typography>
                  )}
                  <Typography variant="subtitle1" gutterBottom>
                    Crash Course:
                  </Typography>
                  <Typography variant="body2" gutterBottom>
                    {currentProblem && currentProblem in problems && problems[currentProblem].description}
                  </Typography>
                </>
              ) : (
                <Typography variant="body1" color="text.secondary">
                  Please select a problem to begin.
                </Typography>
              )}

              <TextField
                multiline
                rows={15}
                fullWidth
                value={code}
                onChange={(e) => setCode(e.target.value)}
                placeholder={currentProblem ? `Write your solution here...` : 'Select a problem to start coding.'}
                variant="outlined"
                sx={{ fontFamily: 'monospace', mt: 2 }}
                disabled={!currentProblem}
              />
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 2 }}>
                <Button
                  variant="contained"
                  color="success"
                  onClick={handleRunCode}
                  disabled={!currentProblem}
                >
                  Run Code
                </Button>
              </Box>
              <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
                Output: {output}
              </Typography>
            </Paper>
          </motion.div>
        </Grid>
      </Grid>

      <Box sx={{ position: 'fixed', bottom: 0, width: '100%' }}>
        <LinearProgress variant="determinate" value={progress} />
        <Typography align="center" sx={{ py: 1 }}>
          Progress: {progress}%
        </Typography>
      </Box>
    </Box>
  );
};

export default HaskellITS;