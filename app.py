from flask import Flask, render_template, request
import io
import sys
import traceback

app= Flask(__name__)

@app.route('/', methods=["GET","POST"])
def home():
    if(request.method=="GET"):
        return render_template('index.html', code="", output="")
    else:
        code=request.form['code']
        runfile=""
        for line in code.splitlines():
            runfile+=line+"\n"
        
        output=io.StringIO()
        sys.stdout=output

        try:
            exec(runfile)
        except Exception as e:
            print(f"An error occurred: {e}")
            formatted_trace=traceback.format_exc()
            formatted_trace=formatted_trace.replace("<string>","solution.py")
            tracelines=formatted_trace.splitlines()
            relevant_trace=["Traceback (most recent call last):"]
            capturing=False
            for line in tracelines:
                if(capturing):
                    relevant_trace.append(line)
                if("exec(runfile)" in line):
                    capturing=True
            clean_trace="\n".join(relevant_trace)
            output.write(clean_trace)
        finally:
            sys.stdout=sys.__stdout__
        print(output.getvalue())
        return render_template("index.html", code=code , output=output.getvalue())
app.run()