# Elena
The final project of CS520. This is a navigation systems optimize for the shortest or fastest route.

## Dependencies
```bash
python = 3.7
flask
OSMnx(https://github.com/gboeing/osmnx)
```

## Usage
Under the root directory, run:
```bash
flask run
```

and use browser to visit: http://127.0.0.1:5000/


## Test
Use this command to change the permission for scripts
```
chmod 777 scripts/foo.sh
```

Run tests with ./scripts/test.sh script. No parameter will run all tests and you could give a directory to run the tests inside a folder. e.g.:
```
# run all tests
./scripts/test.sh

# run model tests
./scripts/test.sh tests/model
```