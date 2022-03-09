int VectorAdd(queue &q, const IntVector &a_vector, const IntVector &b_vector,
               IntVector &sum_parallel, IntVector &flag) {
  // Create the range object for the vectors managed by the buffer.
  range<1> num_items{a_vector.size()};
  // Create buffers that hold the data shared between the host and the devices.
  // The buffer destructor is responsible to copy the data back to host when it
  // goes out of scope.
  buffer a_buf(a_vector);
  buffer b_buf(b_vector);
  buffer sum_buf(sum_parallel.data(), num_items);
  //buffer f_buf(flag.data(), num_items/2);

  // Submit a command group to the queue by a lambda function that contains the
  // data access permission and device computation (kernel).
  std::cout << "Kerenel start... \n";
  q.submit([&](handler &h) {
    // Create an accessor for each buffer with access permission: read, write or
    // read/write. The accessor is a mean to access the memory in the buffer.
    accessor a(a_buf, h, read_only);
    accessor b(b_buf, h, read_only);

    // The sum_accessor is used to store (with write permission) the sum data.
    accessor sum(sum_buf, h, write_only, no_init);
    //accessor flag_kernel(f_buf, h, write_only, no_init);
    // Use parallel_for to run vector addition in parallel on device. This
    // executes the kernel.
    //    1st parameter is the number of work items.
    //    2nd parameter is the kernel, a lambda that specifies what to do per
    //    work item. The parameter of the lambda is the work item id.
    // DPC++ supports unnamed lambda kernel by default.

    h.parallel_for(num_items, [=](auto i) { sum[i] = a[i] + b[i];
                                            if (sum[i]<0){
                                                bool flag=true;
                                                MyDeviceToHostSideChannel::write(i,flag); //Undo, write need to be cleaned out. Right now can only store for 8 overflow.
                                                if (flag) {sum[0]=sum[0]+1;}
                                                }
                                          }
                  );

  });
  bool read_flag=true;
  int interested = 0;
  q.wait();
  std::cout<<sum_parallel[0]<<" Overflow were found.\n";

  interested = 2;

  return interested;

}