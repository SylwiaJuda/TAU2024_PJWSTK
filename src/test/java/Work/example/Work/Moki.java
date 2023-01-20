package Work.example.Work;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.awt.*;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.InstanceOfAssertFactories.LIST;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
public class Moki {
    @Mock
    private  EmployeeStorage employeeStorage;

    @InjectMocks
    private EmployeeService employeeService;

    @Test
    void addEmployeWithEgzistingId(){
        List<Employee> employees = new ArrayList<>();
        employees.add((new Employee(1,22,"Sprzedawca",Department.SALES)));
        when(employeeStorage.getEmployeeList()).thenReturn(employees);
        var reult = employeeService.addEmployee(1,22,"Sprzedawca",Department.SALES);
        assertThat(reult).isEqualTo(null);
    }
}
