from datetime import datetime
import os
import csv
import tkinter as tk
from tkinter import ttk
from decimal import Decimal, InvalidOperation

# Main Code

class LabelInput(tk.Frame):
    """A widget containing a label and input together"""

    def __init__(self,parent, label = '', input_class = ttk.Entry,
                 input_var = None, input_args = None, label_args = None,
                 **kwargs):
        super().__init__(parent, **kwargs)
        input_args = input_args or {}
        label_args = label_args or {}
        self.variable = input_var

        if input_class in (ttk.Checkbutton, ttk.Button, ttk.Radiobutton):
            input_args['text'] = label
            input_args['variable'] = input_var
        else:
            self.label = ttk.Label(self, text = label, **label_args)
            self.label.grid(row = 0, column = 0, sticky = (tk.W + tk.E))
            input_args['textvariable'] = input_var

        self.input = input_class(self, **input_args)
        self.input.grid(row = 1, column = 0, sticky = (tk.W + tk.E))

        self.columnconfigure(0, weight = 1)

        self.error = getattr(self.input, 'error', tk.StringVar())
        self.error_label = ttk.Label(self, textvariable = self.error)
        self.error_label.grid(row = 2, column = 0, sticky = (tk.W + tk.E))

    def grid(self, sticky = (tk.E + tk.W), **kwargs):
        super().grid(sticky = sticky, **kwargs)

    def get(self):
        try:
            if self.variable:
                return self.variable.get()
            elif type(self.input) == tk.Text:
                return self.input.get('1.0', tk.END)
            else:
                return self.input.get()
        except(TypeError, tk.TclError):
            #This happens when numeric fields are empty.
            return ''

    def set(self, value, *args, **kwargs):
        if type(self.variable) == tk.BooleanVar:
            self.variable.set(bool(value))
        elif self.variable:
            self.variable.set(value, *args, **kwargs)
        elif type(self.input) in (ttk.Checkbutton, ttk.Radiobutton):
            if value:
                self.input.select()
            else:
                self.input.deselect()
        elif type(self.input) == tk.Text:
            self.input.delete('1.0', tk.END)
            self.input.insert('1.0', value)
        else:
            #This is to ensure an Entry widget with no variable
            self.input.delete(0, tk.END)
            self.input.insert(0, value)

        
class DataRecordForm(tk.Frame):
    """The Input form of the widgets"""

    def __init__(self,parent,*args,**kwargs):
        super().__init__(parent, *args, **kwargs)

        #A dictionary to keep track of the input widgets
        self.inputs = {}

        #Record Data
        recordinfo = tk.LabelFrame(self, text = 'Record Information', font = ('Verdana', 10))
        #First Row
        self.inputs['Date'] = LabelInput(recordinfo,'Date',input_class = ValidatedDateEntry,
                                         input_var = tk.StringVar())
        self.inputs['Date'].grid(row = 0, column = 0)

        self.inputs['Time'] = LabelInput(recordinfo, 'Time',
                                         input_class = ValidatedCombobox,
                                         input_var = tk.StringVar(),
                                         input_args = {'values':
                                                       ['08:00', '12:00', '16:00', '20:00']})
        self.inputs['Time'].grid(row = 0, column = 1, padx = 10)

        self.inputs['Technician'] = LabelInput(recordinfo, 'Technician', input_class = ValidatedEntry,
                                               input_var = tk.StringVar())
        self.inputs['Technician'].grid(row = 0, column = 2)

        #Second Row
        self.inputs['Lab'] = LabelInput(recordinfo, 'Lab', input_class = ValidatedCombobox,
                                        input_var = tk.StringVar(), input_args = {'values':
                                                                                  ['A','B','C','D','E']})
        self.inputs['Lab'].grid(row = 1, column = 0)

        self.inputs['Plot'] = LabelInput(recordinfo, 'Plot', input_class = ValidatedCombobox,
                                         input_var = tk.StringVar(), input_args = {'values':
                                                                             [str(x) for x in range(1,21)]})
        self.inputs['Plot'].grid(row = 1, column = 1, padx = 10)

        self.inputs['Seed Sample'] = LabelInput(recordinfo, 'Seed Sample', input_class = ValidatedEntry,
                                                input_var = tk.StringVar())
        self.inputs['Seed Sample'].grid(row = 1, column = 2)

        recordinfo.grid(row = 0, column = 0, sticky = tk.W + tk.E)

        #Environment Data
        environinfo = tk.LabelFrame(self, text = 'Environment Information', font = ('Verdana', 10))
        
        self.inputs['Humidity'] = LabelInput(environinfo, 'Humidity(g/m**3)',
                                             input_class = ValidatedSpinbox, input_var = tk.DoubleVar(),
                                             input_args = {'from_':'0.5', 'to':'52.0', 'increment': '.1'})
        self.inputs['Humidity'].grid(row = 0, column = 0)

        self.inputs['Light'] = LabelInput(environinfo, 'Light(kilolux)', input_class = ValidatedSpinbox, input_var = tk.DoubleVar(),
                                          input_args = {'from_':'0', 'to':'100', 'increment':'.1'})
        self.inputs['Light'].grid(row = 0, column = 1, padx = 10)

        self.inputs['Temperature'] = LabelInput(environinfo, 'Temperature(Celcius)', input_class = ValidatedSpinbox, input_var = tk.DoubleVar(),
                                                input_args = {'from_':'4', 'to':'40', 'increment':'.1'})
        self.inputs['Temperature'].grid(row = 0, column = 2)

        self.inputs['Equipment Fault'] = LabelInput(environinfo, 'Equipment Fault',
                                                    input_class = ttk.Checkbutton,
                                                    input_var = tk.BooleanVar())
        self.inputs['Equipment Fault'].grid(row = 1, column = 0, columnspan = 3)

        environinfo.grid(row = 1, column = 0, sticky = tk.W + tk.E)

        #Plant Data
        plantinfo = tk.LabelFrame(self, text = 'Plant Information', font = ('Verdana', 10))

        self.inputs['Plants'] = LabelInput(plantinfo, 'Plants', input_class = ValidatedSpinbox,
                                           input_var = tk.IntVar(), input_args = {'from_': '0', 'to':'20'})
        self.inputs['Plants'].grid(row = 0, column = 0)

        self.inputs['Blossoms'] = LabelInput(plantinfo, 'Blossoms', input_class = ValidatedSpinbox,
                                             input_var = tk.IntVar(), input_args = {'from_':'0', 'to':'1000'})
        self.inputs['Blossoms'].grid(row = 0, column = 1, padx = 10)

        self.inputs['Fruit'] = LabelInput(plantinfo, 'Fruit', input_class = ValidatedSpinbox,
                                          input_var = tk.IntVar(), input_args = {'from_':'0', 'to':'1000'})
        self.inputs['Fruit'].grid(row = 0, column = 2)

        min_height_var = tk.DoubleVar(value = '-infinity')
        max_height_var = tk.DoubleVar(value = 'infinity')

        self.inputs['Min Height'] = LabelInput(plantinfo, 'Min Height(cm)', input_class = ValidatedSpinbox,
                                               input_var = tk.DoubleVar(), input_args = {'from_':'0', 'to':'1000', 'increment': '.1',
                                                                                         'max_var' : max_height_var, 'focus_update_var' : min_height_var})
        self.inputs['Min Height'].grid(row = 1, column = 0)

        self.inputs['Median Height'] = LabelInput(plantinfo, 'Median Height(cm)', input_class = ValidatedSpinbox,
                                                  input_var = tk.DoubleVar(), input_args = {'from_':'0', 'to':'1000', 'increment':'.1',
                                                                                            'min_var' : min_height_var, 'max_var' : max_height_var})
        self.inputs['Median Height'].grid(row = 1, column = 1, padx = 10)

        self.inputs['Max Height'] = LabelInput(plantinfo, 'Max Height(cm)', input_class = ValidatedSpinbox,
                                               input_var = tk.DoubleVar(), input_args = {'from_':'0', 'to':'1000', 'increment':'.1',
                                                                                         'focus_update_var' : max_height_var})
        self.inputs['Max Height'].grid(row = 1, column = 2)

        plantinfo.grid(row = 2, column = 0, sticky = tk.W + tk.E)

        #Notes Section
        self.inputs['Notes'] = LabelInput(self, 'Notes', input_class = tk.Text, input_args = {'width':55, 'height':10})
        self.inputs['Notes'].grid(sticky = 'w', row = 3, column = 0)

        self.reset()

    def get(self):
        data = {}
        for key, widget in self.inputs.items():
            data[key] = widget.get()
        return data

    def reset(self):
        #Saves former session inputs
        lab = self.inputs['Lab'].get()
        time = self.inputs['Time'].get()
        technician = self.inputs['Technician'].get()
        plot = self.inputs['Plot'].get()
        plot_values = self.inputs['Plot'].input.cget('values')

        for widget in self.inputs.values(): #Clear All Fields
            widget.set('')

        todays_date = datetime.today().strftime('%Y/%m/%d')
        self.inputs['Date'].set(todays_date)
        self.inputs['Time'].input.focus()

        #Auto Fills former session inputs if available
        if plot not in ('', plot_values[-1]):
            self.inputs['Lab'].set(lab)
            self.inputs['Time'].set(time)
            self.inputs['Technician'].set(technician)
            next_plot_index = plot_values.index(plot) + 1
            self.inputs['Plot'].set(plot_values[next_plot_index])
            self.inputs['Seed Sample'].input.focus()

    def get_errors(self):
        errors = {}
        for key,widget in self.inputs.items():
            if hasattr(widget.input, 'trigger_focusout_validation'):
                widget.input.trigger_focusout_validation()
            if widget.error.get():
                errors[key] = widget.error.get()
        return errors
        
class ValidationMixin():
    """Adds a validation functionality to an input widget"""

    def __init__(self, *args, error_var = None, **kwargs):
        self.error = error_var or tk.StringVar()
        super().__init__(*args, **kwargs)

        vcmd = self.register(self._validate)
        invcmd = self.register(self._invalid)

        self.config(validate = 'all',
                    validatecommand = (vcmd,'%P','%s','%S','%V','%i','%d'),
                    invalidcommand = (invcmd,'%P','%s','%S','%V','%i','%d'))
        
    def _toggle_error(self, on = False):
        self.config(foreground = ('red' if on else 'black'))

    def _validate(self, proposed, current, char , event, index, action):
        self._toggle_error(False)
        self.error.set('')
        valid = True

        if event == 'focusout':
            valid = self._focusout_validate(event = event)
        elif event == 'key':
            valid = self._key_validate(proposed = proposed, current = current, char = char, event = event, index = index, action = action)
        return valid

    def _focusout_validate(self, **kwargs):
        return True

    def _key_validate(self, **kwargs):
        return True

    def _invalid(self, proposed, current, char, event, index, action):
        if event == 'focusout':
            self._focusout_invalid(event = event)
        elif event == 'key':
            self._key_invalid(proposed = proposed, current = current, char = char, event = event, index = index, action = action)

    def _focusout_invalid(self, **kwargs):
        self._toggle_error(True)

    def _key_invalid(self, **kwargs):
        pass

    def trigger_focusout_validation(self):
        valid = self._validate('','','','focusout','','')
        if not valid:
            self._focusout_invalid(event = 'focusout')
        return valid


class ValidatedEntry(ValidationMixin, ttk.Entry):

    def _focusout_validate(self, event):
        valid = True
        if not self.get():
            valid = False
            self.error.set('A value is required!')
        return valid

    
class ValidatedDateEntry(ValidationMixin, ttk.Entry):

    def _key_validate(self, action, index, char, **kwargs):
        valid = True

        if action == '0':  #Deleting any value should validate
            valid = True
        elif index in ('0','1','2','3','5','6','8','9'):
            valid = char.isdigit()
        elif index in ('4','7'):
            valid = char == '/'
        else:
            valid = False
        return valid

    def _focusout_validate(self, event):
        valid = True
        if not self.get():
            self.error.set('An input is required!')
            valid = False
        try:
            datetime.strptime(self.get(), '%Y/%m/%d')
        except ValueError:
            self.error.set('Invalid Date')
            valid = False
        return valid


class ValidatedCombobox(ValidationMixin, ttk.Combobox):

    def _key_validate(self, proposed, action, **kwargs):
        valid = True

        if action == '0':
            self.set('') #Delete or Backspace clears the field
            return True

        #Get the values
        values = self.cget('values')

        matching = [ x for x in values if x.lower().startswith(proposed.lower())]
        if len(matching) == 0:
            valid = False
        elif len(matching) == 1:
            self.set(matching[0])
            self.icursor(tk.END)
            valid = True
        return valid

    def _focusout_validate(self, **kwargs):
        valid = True

        if not self.get():
            valid = False
            self.error.set('An entry is required!')
        return valid

    
class ValidatedSpinbox(ValidationMixin, ttk.Spinbox):

    def __init__(self, *args, min_var = None, max_var = None, focus_update_var = None, from_ = '-Infinity', to = 'Infinity', **kwargs):
        super().__init__(*args, from_ = from_, to = to, **kwargs)

        self.resolution = Decimal(str(kwargs.get('increment', '1.0')))
        self.precision = (self.resolution.normalize().as_tuple().exponent)

        self.variable = kwargs.get('textvariable') or tk.DoubleVar()

        if min_var:
            self.min_var = min_var
            self.min_var.trace('w', self._set_minimum)
        if max_var:
            self.max_var = max_var
            self.max_var.trace('w', self._set_maximum)
        self.focus_update_var = focus_update_var
        self.bind('<FocusOut>', self._set_focus_update_var)

    def _set_focus_update_var(self, event):
        value = self.get()
        if self.focus_update_var and not self.error.get():
            self.focus_update_var.set(value)

    def _set_minimum(self, *args):
        current = self.get()

        try:
            new_min = self.min_var.get()
            self.config(from_ = new_min)
        except (tk.TclError, ValueError):
            pass

        if not current:
            self.delete(0, tk.END)
        else:
            self.variable.set(current)

        self.trigger_focusout_validation()

    def _set_maximum(self, *args):
        current = self.get()

        try:
            new_max = self.max_var.get()
            self.config(to = new_max)
        except (tk.TclError, ValueError):
            pass

        if not current:
            self.delete(0, tk.END)
        else:
            self.variable.set(current)

        self.trigger_focusout_validation()
    

    def _key_validate(self, char, index, current, proposed, action, **kwargs):
        valid = True

        min_val = self.cget('from')
        max_val = self.cget('to')
        no_negative = min_val >= 0
        no_decimal = self.precision >= 0

        if action == '0':
            return True
        
        #Filtering out obviously invalid keystrokes
        if any([ (char not in ('-1234567890')), (char == '-' and (no_negative or index != '0')), (char == '.' and (no_decimal or '.' in current)) ]):
            return False

        if proposed in '-.':
            return True

        #Proposed should be a valid decimal String
        proposed = Decimal(proposed)
        proposed_precision = proposed.as_tuple().exponent

        if any([ (proposed > max_val), (proposed_precision < self.precision) ]):
            return False

        return valid

    def _focusout_validate(self, **kwargs):
        valid = True
        value = self.get()
        min_val = self.cget('from')
        max_val = self.cget('to')

        try:
            value = Decimal(value)
        except InvalidOperation:
            self.error.set('Invalid number string: {}'.format(value))
            return False

        if value < min_val:
            self.error.set('Value is too low (Minimum -> {})'.format(min_val))
            return False
        if value > max_val:
            self.error.set('Value is too high (Maximum -> {})'.format(max_val))
            return False
        
        return valid
            
            
class Application(tk.Tk):
    """Application root window"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title('ABQ Data Entry App')
        self.resizable(width = False, height = False)
        ttk.Label(self, text = 'ABQ Data Entry App', font = ('STENCIL', 18)).grid(row = 0)

        self.recordform = DataRecordForm(self)
        self.recordform.grid(row = 1, padx = 10)

        self.savebutton = ttk.Button(self, text = 'Save', command = self.on_save)
        self.savebutton.grid(sticky = tk.E, row = 2, padx = 10)

        #Status Bar
        self.status = tk.StringVar()
        self.statusbar = ttk.Label(self, textvariable = self.status)
        self.statusbar.grid(sticky = (tk.W + tk.E), row = 3, padx = 10)

        self.records_saved = 0
        
    def on_save(self):
        errors = self.recordform.get_errors() #Check for Errors first.
        if errors:
            self.status.set('Cannot Save due to errors in field(s): {}'.format(','.join(errors.keys())))
            return False
        
        datestring = datetime.today().strftime('%Y-%m-%d')
        filename = 'abq_data_record_{}.csv'.format(datestring)
        newfile = not os.path.exists(filename)

        data = self.recordform.get()
        with open(filename,'a') as fh:
            csvwriter = csv.DictWriter(fh, fieldnames = data.keys())
            if newfile:
                csvwriter.writeheader()
            csvwriter.writerow(data)
        self.records_saved += 1
        self.status.set('{} record(s) saved during this session'.format(self.records_saved))

        self.recordform.reset()

        
if __name__ == '__main__' :
    app = Application()
    app.mainloop()